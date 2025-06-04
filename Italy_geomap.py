import streamlit as st
import pandas as pd
import folium 
from streamlit_folium import st_folium





st.set_page_config(page_title="Italy Hotels Map", page_icon="🗺️", layout="wide")


@st.cache_data
def load_data():
    link = "C://Users/LENOVO/OneDrive/Bureau/Streamlit/Geo_data/hotel_listings_Italy.csv"
    df = pd.read_csv(link, encoding="ISO-8859-1")
    star_labels = {
    "OneStar": "⭐",
    "TwoStar": "⭐⭐",
    "ThreeStar": "⭐⭐⭐",
    "FourStar": "⭐⭐⭐⭐",
    "FiveStar": "⭐⭐⭐⭐⭐",
    "All": "B&B"}
    df[" HotelRating_labels"] = df[" HotelRating"].map(star_labels)
    #df = df[(df[" HotelRating"] == "FiveStar")]
    df = df.sample(frac=0.1, random_state=42)
    
    return df

df = load_data()


st.title("🗺️ Italy Hotel Listings")

page = st.sidebar.radio("Select Page", ["🏠 Main", "🗂️ About The Dataset"])


st.markdown(
    """
    <style>
    div[data-testid="column"]:nth-of-type(2) {
        text-align: end;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if page == "🏠 Main":
    st.sidebar.header("🔍 Filter Hotels")
    region_filter = st.sidebar.selectbox("Select Region", ["All"] + list(df["region"].dropna().unique()))
    rating_filter = st.sidebar.multiselect(
    label="Select Rating",
    options=df[" HotelRating_labels"].unique(),
    default=df[" HotelRating_labels"].unique())
    
    if region_filter == "All":
        filtered_df = df[df[" HotelRating_labels"].isin(rating_filter)]
    else:
        filtered_df = df[(df["region"] == region_filter) & (df[" HotelRating_labels"].isin(rating_filter))]
    filtered_df = filtered_df.sort_values(by=" HotelName")
    italy_coordinates = [41.873988, 12.564167]
    italy_bounds = [[35.5, 5], [47.5, 20]]
    Italy_map = folium.Map(italy_coordinates, zoom_start=8, max_bounds=italy_bounds)
    Italy_map.fit_bounds(italy_bounds)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="fixed-map">', unsafe_allow_html=True)
        st.subheader("📌 Click on the location for more details!")
        for _, row in filtered_df.iterrows():
            hotels_popup = f"""
            <b>{row[' HotelName']}</b></br>
            Rating: {row[' HotelRating_labels']}</br>
            📍 Adress : {row[' Address']} </br>
            🔗 <a href='{row[' HotelWebsiteUrl']}' target='_blank'>Hotel Website</a>
            """
            folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=3,  
            color="pink",
            fill=True,
            fill_color="blue",
            popup=folium.Popup(hotels_popup, max_width=400)
            ).add_to(Italy_map)
            
        st_map = st_folium(Italy_map, width=725)


    with col2:
        st.write(" ")
        st.subheader("🏛️ Must-Visit Destinations in Italy ")
        st.write("    ")
        st.write("")
        cities =[{
        "name": "Rome",
        "description": "Rome, the Eternal City, is a treasure trove of history, art, and culture.",
        "guide_link": "https://www.rome.net",
        "image_url": "https://images.unsplash.com/photo-1555992828-ca4dbe41d294?q=80&w=1064&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        },
        {
        "name": "Milan",
        "description": "Milan is Italy's fashion capital, known for its high-end shopping, art, and design scene.",
        "guide_link": "https://www.turismo.milano.it",
        "image_url": "https://images.unsplash.com/photo-1513581166391-887a96ddeafd?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        },
        {
        "name": "Como",
        "description": "Como is a charming lakeside city, famous for its stunning lake views and picturesque landscapes.",
        "guide_link": "https://www.lakecomo.it",
        "image_url": "https://images.unsplash.com/photo-1537535261941-f2cbdb39bd83?q=80&w=987&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        },
        {
        "name": "Florence",
        "description": "Florence is a cradle of Renaissance art and architecture, home to iconic landmarks like the Uffizi Gallery.",
        "guide_link": "https://www.visitflorence.com",
        "image_url": "https://images.unsplash.com/photo-1537366057310-3501fc868fd8?q=80&w=1015&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        },
        {
        "name": "Naples",
        "description": "Naples is a vibrant city known for its rich history, pizza, and proximity to the Amalfi Coast.",
        "guide_link": "https://www.turismo.na.it",
        "image_url": "https://images.unsplash.com/photo-1572984446446-68afa780b1d9?q=80&w=1935&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        },
        {
        "name": "Verona",
        "description": "Verona is a romantic city, home to the famous Juliet's house and a stunning Roman amphitheater.",
        "guide_link": "https://www.comune.verona.it",
        "image_url": "https://images.unsplash.com/photo-1551806580-e668327b0611?q=80&w=1169&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        },
        {
        "name": "Venice",
        "description": "Venice is a unique city built on water, known for its canals, gondola rides, and the beautiful St. Mark's Square.",
        "guide_link": "https://www.veneziaunica.it",
        "image_url": "https://images.unsplash.com/photo-1558271736-cd043ef2e855?q=80&w=1031&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        },
        {
        "name": "Positano",
        "description": "Positano is a stunning cliffside village on the Amalfi Coast, known for its colorful buildings and breathtaking views.",
        "guide_link": "https://www.positano.com",
        "image_url": "https://plus.unsplash.com/premium_photo-1677359735525-41758ffe51c8?q=80&w=1070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        },
        {
        "name": "Capri",
        "description": "Capri is a beautiful island in the Bay of Naples, famous for its dramatic cliffs, blue grotto, and upscale shopping.",
        "guide_link": "https://www.capri.com",
        "image_url": "https://plus.unsplash.com/premium_photo-1673138835852-12eb32d97d3d?q=80&w=1936&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        },
        {
        "name": "Sardinia",
        "description": "Sardinia is an island known for its pristine beaches, ancient ruins, and mountainous landscapes.",
        "guide_link": "https://www.sardegnaturismo.it",
        "image_url": "https://images.unsplash.com/photo-1557207411-58bf12d9079f?q=80&w=987&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        },
        {
        "name": "Sicily",
        "description": "Sicily, Italy's largest island, offers a mix of ancient ruins, beautiful beaches, and vibrant cultural heritage.",
        "guide_link": "https://www.visitsicily.info",
        "image_url": "https://images.unsplash.com/photo-1523365154888-8a758819b722?q=80&w=1169&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        },]
        with st.container(border=False, height=710): 
            for city in cities:
                with st.container(border=True):
                    st.markdown('<div class="sticky-container">', unsafe_allow_html=True)
                    st.title(f"**{city['name']}**")
                    st.write(city['description'])
                    st.markdown(f"[Explore {city['name']}]({city['guide_link']})", unsafe_allow_html=True)
                    st.image(city['image_url'], caption=f"{city['name']}")
    
if page == "🗂️ About The Dataset":
    link_to_dataset = "https://www.kaggle.com/datasets/raj713335/tbo-hotels-dataset"
    link_to_geofile = "https://github.com/openpolis/geojson-italy/blob/master/geojson/limits_IT_regions.geojson"
    st.subheader("About The Data:")
    st.write("This dataset has can be found on Kaggle [here](%s). It contains 1,000,000+ hotels listings aroundthe world with numerous information about hotel names, adresses, ratings, links, etc. It has 16 columns in total."% link_to_dataset)
    st.write("I've had already done some basic data wrangling on this dataset previously: \n - I have filtered the countries to only keep Italy as it is our zone of interest.\n - I have removed missing data \n - Since we have our coordinates in one variable, I have created two seperate variables to work with folium later on. \n - Using the coordinates, I have also used Geopandas to get the region of each hotel to create a region filter afterwards. For this I used this [file](%s)."%link_to_geofile)
    st.info("Note : The original listing file is larger, I only took a sample (20%) to display it here.")
    


    
    







   



