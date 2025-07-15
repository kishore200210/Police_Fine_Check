
import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# Connect to MySQL
def st_connect():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="police"
        )
        return mydb
    except mysql.connector.Error as e:
        st.error(f"Connection error: {e}")
        return None

# Fetch data from MySQL
def fetch_data(query):
    conn = st_connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(data, columns=columns)
        finally:
            conn.close()
    return pd.DataFrame()

import streamlit as st

# Set background image using CSS
import streamlit as st
# Streamlit UI
import plotly.express as px
import base64
import os

# Set page config
st.set_page_config(layout="wide", page_title="Police Challan Dashboard")

# ----------------------------------------
# Background Image Function
# ----------------------------------------
def add_bg_from_local(image_file):
    if not os.path.exists(image_file):
        st.warning(f"Background image not found: {image_file}")
        return
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

import os

# This will always work no matter where you run from
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "D:\workspace\Environment\Scripts\WhatsApp Image 2025-07-15 at 01.15.27_91981ae8.jpg")

add_bg_from_local(image_path)


#st.title(" Police challan checking")
st.markdown("<h1 style='color:red; font-size:48px;'>Police Challan Checking</h1>", unsafe_allow_html=True)


menu = st.sidebar.selectbox("Select Option", [
    "All Data", 
    "Top Drug Vehicles", 
    "Violation Chart", 
    "Arrest Analysis",
    "Age Group Arrest Analysis",
    "gender combination has the highest search rate",
    "most traffic stops",
    "average stop duration for different violations",
    "Are stops during the night more likely to lead to arrests",
    "Which violations are most associated with searches or arrests?",
    "Which violations are most common among younger drivers (<25)?",
    "Is there a violation that rarely results in search or arrest?",
    "Which countries report the highest rate of drug-related stops?",
    "What is the arrest rate by country and violation?",
    "Which country has the most stops with search conducted?",
])

complex = st.sidebar.selectbox("Select Option", [
    
    "Yearly Breakdown of Stops and Arrests by Country",
    "Driver Violation Trends Based on Age and Race",
    "Time Period Analysis of Stops",
    "Violations with High Search and Arrest Rates",
    "Driver Demographics by Country",
    "Top 5 Violations with Highest Arrest Rates",

])


if menu == "All Data":
    df = fetch_data("SELECT * FROM fine")
    st.dataframe(df)

elif menu == "Top Drug Vehicles":
    query = """
    SELECT vehicle_number, COUNT(*) AS total
    FROM fine
    WHERE drugs_related_stop = TRUE
    GROUP BY vehicle_number
    ORDER BY total DESC
    LIMIT 10
    """
    df = fetch_data(query)
    st.bar_chart(df.set_index("vehicle_number"))

elif menu == "Violation Chart":
    query = """
    SELECT violation, COUNT(*) AS total
    FROM fine
    GROUP BY violation
    ORDER BY total DESC

    """
    df = fetch_data(query)
    fig = px.bar(df, x="violation", y="total", title="Violation Frequency", color="total")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Arrest Analysis":
    query = """
    SELECT country_name, driver_gender, COUNT(*) AS stop_count
    FROM fine
    GROUP BY country_name, driver_gender
    ORDER BY country_name, driver_gender;

    """
    df = fetch_data(query)
    st.dataframe(df)


elif menu == "Age Group Arrest Analysis":
    query = """
    SELECT 
      CASE 
        WHEN driver_age < 18 THEN 'Under 18'
        WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
        WHEN driver_age BETWEEN 26 AND 40 THEN '26-40'
        WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
        ELSE '60+' 
      END AS age_group,
      COUNT(*) AS total,
      SUM(is_arrested) AS arrested,
      ROUND(SUM(is_arrested) * 100.0 / COUNT(*), 2) AS arrest_rate
    FROM fine
    GROUP BY age_group
    ORDER BY arrest_rate DESC
    """
    df = fetch_data(query)
    st.dataframe(df)


elif menu == "gender combination has the highest search rate":
    query = """

    SELECT  driver_race, driver_gender, COUNT(*) AS total_stops,
    SUM(search_conducted) AS total_searches,
    ROUND(SUM(search_conducted) * 100.0 / COUNT(*), 2) AS search_rate
    FROM fine
    GROUP BY driver_race, driver_gender
    ORDER BY search_rate DESC
    LIMIT 1;

    
    """
    df = fetch_data(query)
    st.dataframe(df)

elif menu == "most traffic stops":
    query = """

    SELECT HOUR(stop_time) AS hour_of_day,
    COUNT(*) AS stop_count
    FROM fine
    GROUP BY hour_of_day
    ORDER BY stop_count DESC;

    """
    df = fetch_data(query)
    st.dataframe(df)


elif menu == "average stop duration for different violations":
    query = """
    SELECT violation,
           AVG(CASE 
               WHEN stop_duration = '0-15 Min' THEN 7.5
               WHEN stop_duration = '16-30 Min' THEN 23
               WHEN stop_duration = '30+ Min' THEN 45
               ELSE NULL
           END) AS avg_duration_minutes
    FROM fine
    GROUP BY violation
    ORDER BY avg_duration_minutes DESC;
    """
    df = fetch_data(query)
    st.dataframe(df)

elif menu == "Are stops during the night more likely to lead to arrests":
    query = """
    SELECT CASE 
    WHEN HOUR(stop_time) BETWEEN 6 AND 17 THEN 'Day'
    ELSE 'Night'
    END AS time_of_day,
    COUNT(*) AS total_stops,
    SUM(is_arrested) AS total_arrests,
    ROUND(SUM(is_arrested) * 100.0 / COUNT(*), 2) AS arrest_rate
    FROM fine
    GROUP BY time_of_day
    ORDER BY arrest_rate DESC;

    """
    df = fetch_data(query)
    st.dataframe(df)

elif menu == "Which violations are most associated with searches or arrests?":
    query = """

    SELECT 
    violation,
    COUNT(*) AS total_stops,
    SUM(search_conducted) AS total_searches,
    SUM(is_arrested) AS total_arrests,
    ROUND(SUM(search_conducted) * 100.0 / COUNT(*), 2) AS search_rate,
    ROUND(SUM(is_arrested) * 100.0 / COUNT(*), 2) AS arrest_rate
    FROM fine
    GROUP BY violation
    ORDER BY search_rate DESC, arrest_rate DESC;

    """
    df = fetch_data(query)
    st.dataframe(df)

elif menu == "Which violations are most common among younger drivers (<25)?":
    query = """

    SELECT 
    violation,
    COUNT(*) AS total_violations
    FROM fine
    WHERE driver_age < 25
    GROUP BY violation
    ORDER BY total_violations DESC;

    """
    df = fetch_data(query)
    st.dataframe(df)

elif menu == "Is there a violation that rarely results in search or arrest?":
    query = """

    SELECT 
    violation,
    COUNT(*) AS total_stops,
    SUM(search_conducted) AS total_searches,
    SUM(is_arrested) AS total_arrests,
    ROUND(SUM(search_conducted) * 100.0 / COUNT(*), 2) AS search_rate,
    ROUND(SUM(is_arrested) * 100.0 / COUNT(*), 2) AS arrest_rate
    FROM fine
    GROUP BY violation
    HAVING search_rate < 5 AND arrest_rate < 5
    ORDER BY total_stops DESC;

    """
    df = fetch_data(query)
    st.dataframe(df)

elif menu == "Which countries report the highest rate of drug-related stops?":
    query="""

    SELECT 
    country_name,
    COUNT(*) AS total_stops,
    SUM(drugs_related_stop) AS drug_stops,
    ROUND(SUM(drugs_related_stop) * 100.0 / COUNT(*), 2) AS drug_stop_rate
    FROM fine
    GROUP BY country_name
    ORDER BY drug_stop_rate DESC;

    """
    df = fetch_data(query)
    st.dataframe(df)

elif menu == "What is the arrest rate by country and violation?":
    query="""

    SELECT 
    country_name,
    violation,
    COUNT(*) AS total_stops,
    SUM(is_arrested) AS total_arrests,
    ROUND(SUM(is_arrested) * 100.0 / COUNT(*), 2) AS arrest_rate
    FROM fine
    GROUP BY country_name, violation
    ORDER BY arrest_rate DESC;

    """
    df = fetch_data(query)
    st.dataframe(df)

elif menu == "Which country has the most stops with search conducted?":
    query="""

    SELECT 
    country_name,
    COUNT(*) AS total_searches
    FROM fine
    WHERE search_conducted = TRUE
    GROUP BY country_name
    ORDER BY total_searches DESC
    LIMIT 1;

    """
    df = fetch_data(query)
    st.dataframe(df)

if complex == "Yearly Breakdown of Stops and Arrests by Country":
    query="""
    SELECT 
    country_name,
    YEAR(stop_date) AS year,
    COUNT(*) AS total_stops,
    SUM(is_arrested) AS total_arrests,
    ROUND(SUM(is_arrested) * 100.0 / COUNT(*), 2) AS arrest_rate
    FROM fine
    GROUP BY country_name, YEAR(stop_date)
    ORDER BY country_name, year;

    """
    df = fetch_data("SELECT * FROM fine")
    st.dataframe(df)

elif complex == "Driver Violation Trends Based on Age and Race":
    query="""

    SELECT 
    driver_race,
    CASE 
    WHEN driver_age < 18 THEN 'Under 18'
    WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
    WHEN driver_age BETWEEN 26 AND 40 THEN '26-40'
    WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
    ELSE '60+'
    END AS age_group,
    violation,
    COUNT(*) AS total_violations
    FROM fine
    GROUP BY driver_race, age_group, violation
    ORDER BY driver_race, age_group, total_violations DESC;

    """
    df = fetch_data(query)
    st.dataframe(df)

elif complex == "Time Period Analysis of Stops":
    query="""

    SELECT 
    YEAR(stop_date) AS year,
    MONTH(stop_date) AS month,
    HOUR(stop_time) AS hour,
    COUNT(*) AS total_stops
    FROM fine
    GROUP BY year, month, hour
    ORDER BY year, month, hour;

    """
    df = fetch_data(query)
    st.dataframe(df)

elif complex == "Violations with High Search and Arrest Rates":
    query="""
    SELECT *
    FROM (
    SELECT 
        violation,
        COUNT(*) AS total_stops,
        SUM(search_conducted) AS total_searches,
        SUM(is_arrested) AS total_arrests,
        ROUND(SUM(search_conducted) * 100.0 / COUNT(*), 2) AS search_rate,
        ROUND(SUM(is_arrested) * 100.0 / COUNT(*), 2) AS arrest_rate,
        ROUND(AVG(SUM(search_conducted) * 100.0 / COUNT(*)) OVER (), 2) AS avg_search_rate,
        ROUND(AVG(SUM(is_arrested) * 100.0 / COUNT(*)) OVER (), 2) AS avg_arrest_rate
    FROM fine
    GROUP BY violation
    ) AS stats
    WHERE 
        stats.search_rate > stats.avg_search_rate AND
        stats.arrest_rate > stats.avg_arrest_rate
    ORDER BY stats.search_rate DESC, stats.arrest_rate DESC;

    """
    df = fetch_data(query)
    st.dataframe(df)


elif complex == "Driver Demographics by Country":
    query="""
    
    SELECT 
    country_name,
    driver_gender,
    driver_race,
    COUNT(*) AS total_drivers,
    ROUND(AVG(driver_age), 1) AS average_age
    FROM fine
    GROUP BY country_name, driver_gender, driver_race
    ORDER BY country_name, total_drivers DESC;

    """
    df = fetch_data(query)
    st.dataframe(df)

elif complex == "Top 5 Violations with Highest Arrest Rates":
    query="""
    
    SELECT 
    violation,
    COUNT(*) AS total_stops,
    SUM(is_arrested) AS total_arrests,
    ROUND(SUM(is_arrested) * 100.0 / COUNT(*), 2) AS arrest_rate
    FROM fine
    GROUP BY violation
    HAVING COUNT(*) > 0
    ORDER BY arrest_rate DESC
    LIMIT 5;

    """
    df = fetch_data(query)
    st.dataframe(df)

elif menu == "Custom SQL":
    user_query = st.text_area("Enter your SQL query:")
    if st.button("Run Query"):
        df = fetch_data(user_query)
        st.dataframe(df)

#customizer query
st.sidebar.markdown("### 🔍 Custom Filters")


year_range = st.sidebar.slider("Select Year Range", 2010, 2025, (2015, 2025))


country = st.sidebar.selectbox("Select Country", options=["All"] + sorted(df["country_name"].dropna().unique().tolist()))


gender = st.sidebar.multiselect("Driver Gender", options=df["driver_gender"].dropna().unique().tolist(), default=[])


race = st.sidebar.multiselect("Driver Race", options=df["driver_race"].dropna().unique().tolist(), default=[])


violation = st.sidebar.multiselect("Violation Type", options=df["violation"].dropna().unique().tolist(), default=[])


filtered_df = df.copy()


filtered_df["year"] = pd.to_datetime(filtered_df["stop_date"]).dt.year
filtered_df = filtered_df[filtered_df["year"].between(year_range[0], year_range[1])]

if country != "All":
    filtered_df = filtered_df[filtered_df["country_name"] == country]

if gender:
    filtered_df = filtered_df[filtered_df["driver_gender"].isin(gender)]

if race:
    filtered_df = filtered_df[filtered_df["driver_race"].isin(race)]

if violation:
    filtered_df = filtered_df[filtered_df["violation"].isin(violation)]


st.subheader("📊 Filtered Police Stop Records")
st.dataframe(filtered_df)


import streamlit as st
import pandas as pd
import mysql.connector

@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="police"
    )
    df = pd.read_sql("SELECT * FROM fine", conn)
    conn.close()
    return df

df = load_data()


st.sidebar.title("🔍 Filter Your Search")
year_range = st.sidebar.slider("Year Range", 2010, 2025, (2015, 2025))
country = st.sidebar.selectbox("Country", ["All"] + sorted(df["country_name"].dropna().unique()))
gender = st.sidebar.multiselect("Gender", df["driver_gender"].dropna().unique())
race = st.sidebar.multiselect("Race", df["driver_race"].dropna().unique())
violation = st.sidebar.multiselect("Violation", df["violation"].dropna().unique())


df["year"] = pd.to_datetime(df["stop_date"]).dt.year
filtered = df[df["year"].between(year_range[0], year_range[1])]

if country != "All":
    filtered = filtered[filtered["country_name"] == country]
if gender:
    filtered = filtered[filtered["driver_gender"].isin(gender)]
if race:
    filtered = filtered[filtered["driver_race"].isin(race)]
if violation:
    filtered = filtered[filtered["violation"].isin(violation)]


st.title("📋 Filtered Police Stop Records")
st.dataframe(filtered)
