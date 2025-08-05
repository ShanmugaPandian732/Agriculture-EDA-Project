import streamlit as st
import pandas as pd
import pymysql

# Database Connection
def create_connection():
    try:
        connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'agriculture_db',
            cursorclass = pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None
    
# Fetch Data from Database
def fetch_data(query):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame(result)
                return df
        finally:
            connection.close()
    else:
        return pd.DataFrame()

query = "SELECT * FROM indiacropsdataset"
data = fetch_data(query)

# Streamlit App Title
st.set_page_config(page_title = "Indian States with Districts Agriculture Crops Records", layout = 'wide')

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Project Introduction", "SQL Queries", "Created By"])

# Page 1: introduction
if page == "Project Introduction":

    st.title("🌾 Indian States with Districts Agriculture Crops Records")
    st.image(r"C:\Users\arun prakash\Downloads\1598228.jpg")
    st.subheader("🚦A Streamlit App for Exploring Indian States with Districts Agriculture Crops Records")
    st.write("""
    This project analyzes Agriculture Records from different States using a MYSQL database.
    It provides different Trends, Patterns and Relationships within the Data.
 
    **Features:**
    - View the Agricultural differences between Districts through the States.
    - Generate the different Queries for multiple scenarios.
    - Run SQL queries to explore insights.

    **Database Used:** 'indiacropsdataset.mysql'
    """)
    # ✅ Show dataframe only here
    st.dataframe(data, use_container_width=True)
else:
    print("Project Introduction not found")

#page 2: SQL Queries
if page == "SQL Queries":
    st.title("🗓️ SQL Queries")
    selected_query = st.selectbox("Choose a Query", [
    "Year-wise Trend of Rice Production Across States (Top 3)",
    "Top 5 Districts by Wheat Yield Increase Over the Last 5 Years (2012 - 2017)",
    "States with the Highest Growth in Oilseed Production 5-Year Growth Rate (2012 - 2017)",
    "District-wise Correlation Between Area and Production for Rice",
    "Yearly Production Growth of Cotton in Top 5 Cotton Producing States",
    "Districts with the Highest Groundnut Production in 2017",
    "Annual Average Maize Yield Across All States",
    "Total Area Cultivated for Oilseeds in Each State",
    "Districts with the Highest Rice Yield (2017)",
    "Compare the Production of Wheat and Rice for the Top 5 States Over 10 Years (2008 - 2017)",
])
    simple_query = {
    "Year-wise Trend of Rice Production Across States (Top 3)" : "SELECT d.Year, d.`State Name`, SUM(d.`RICE PRODUCTION (1000 tons)`) AS Total_Rice_Production FROM indiacropsdataset d JOIN (SELECT `State Name` FROM indiacropsdataset GROUP BY `State Name` ORDER BY SUM(`RICE PRODUCTION (1000 tons)`) DESC LIMIT 3) top_states ON d.`State Name` = top_states.`State Name` GROUP BY d.Year, d.`State Name` ORDER BY d.Year, Total_Rice_Production DESC;",
    "Top 5 Districts by Wheat Yield Increase Over the Last 5 Years (2012 - 2017)" : "SELECT t2017.`Dist Name` AS dist_name, (t2017.`WHEAT YIELD (Kg per ha)` - t2012.`WHEAT YIELD (Kg per ha)`) AS yield_increase FROM indiacropsdataset t2012 JOIN indiacropsdataset t2017 ON t2012.`Dist Name` = t2017.`Dist Name` AND t2012.Year = 2012 AND t2017.Year = 2017 ORDER BY yield_increase DESC LIMIT 5;",
    "States with the Highest Growth in Oilseed Production 5-Year Growth Rate (2012 - 2017)" : "SELECT t2017.`State Name` AS state_name, ((SUM(t2017.`OILSEEDS PRODUCTION (1000 tons)`) - SUM(t2012.`OILSEEDS PRODUCTION (1000 tons)`)) / SUM(t2012.`OILSEEDS PRODUCTION (1000 tons)`) * 100) AS growth_percent FROM indiacropsdataset t2012 JOIN indiacropsdataset t2017 ON t2012.`State Name` = t2017.`State Name` AND t2012.`Dist Name` = t2017.`Dist Name` AND t2012.Year = 2012 AND t2017.Year = 2017 GROUP BY t2017.`State Name` ORDER BY growth_percent DESC LIMIT 5;",
    "District-wise Correlation Between Area and Production for Rice" : "SELECT `Dist Name` AS dist_name, ((COUNT(*) * SUM(`RICE AREA (1000 ha)` * `RICE PRODUCTION (1000 tons)`) - SUM(`RICE AREA (1000 ha)`) * SUM(`RICE PRODUCTION (1000 tons)`)) / SQRT((COUNT(*) * SUM(POWER(`RICE AREA (1000 ha)`, 2)) - POWER(SUM(`RICE AREA (1000 ha)`), 2)) * (COUNT(*) * SUM(POWER(`RICE PRODUCTION (1000 tons)`, 2)) - POWER(SUM(`RICE PRODUCTION (1000 tons)`), 2)))) AS correlation FROM indiacropsdataset GROUP BY `Dist Name` HAVING COUNT(*) > 1;",
    "Yearly Production Growth of Cotton in Top 5 Cotton Producing States" : "SELECT `State Name`, Year, SUM(`COTTON PRODUCTION (1000 tons)`) AS total_production FROM indiacropsdataset WHERE `State Name` IN (SELECT `State Name` FROM (SELECT `State Name`, SUM(`COTTON PRODUCTION (1000 tons)`) AS total FROM indiacropsdataset GROUP BY `State Name` ORDER BY total DESC LIMIT 5) AS top_states) GROUP BY `State Name`, Year ORDER BY `State Name`, Year;",
    "Districts with the Highest Groundnut Production in 2017" : "SELECT `Dist Name`, `State Name`, `GROUNDNUT PRODUCTION (1000 tons)` FROM indiacropsdataset WHERE Year = 2017 ORDER BY `GROUNDNUT PRODUCTION (1000 tons)` DESC LIMIT 7;",
    "Annual Average Maize Yield Across All States" : "SELECT `State Name`, Year, AVG(`MAIZE YIELD (Kg per ha)`) AS avg_maize_yield FROM indiacropsdataset GROUP BY `State Name`, Year ORDER BY `State Name`, Year;",
    "Total Area Cultivated for Oilseeds in Each State" : "SELECT `State Name`, SUM(`OILSEEDS AREA (1000 ha)`) AS total_oilseeds_area FROM indiacropsdataset GROUP BY `State Name` ORDER BY total_oilseeds_area DESC;",
    "Districts with the Highest Rice Yield (2017)" : "SELECT `Dist Name`, `State Name`, `RICE YIELD (Kg per ha)` FROM indiacropsdataset WHERE Year = 2017 ORDER BY `RICE YIELD (Kg per ha)` DESC LIMIT 6;",
    "Compare the Production of Wheat and Rice for the Top 5 States Over 10 Years (2008 - 2017)" : "SELECT `State Name`, Year, SUM(`RICE PRODUCTION (1000 tons)`) AS rice_production, SUM(`WHEAT PRODUCTION (1000 tons)`) AS wheat_production FROM indiacropsdataset WHERE `State Name` IN (SELECT `State Name` FROM (SELECT `State Name`, SUM(`RICE PRODUCTION (1000 tons)` + `WHEAT PRODUCTION (1000 tons)`) AS total_prod FROM indiacropsdataset WHERE Year BETWEEN 2008 AND 2017 GROUP BY `State Name` ORDER BY total_prod DESC LIMIT 5) AS top_states) AND Year BETWEEN 2008 AND 2017 GROUP BY `State Name`, Year ORDER BY `State Name`, Year;",  
}
    if st.button("Run Query"):
        result = fetch_data(simple_query[selected_query])
        if not result.empty:
            st.write(result)
        else:
            st.warning("No results found for the selected query.")
else:
    print("SQL Queries was not found")

# page 3: Created By
if page == "Created By":
    st.title("☀️ Creator of this project")
    st.write("""
    **Developed by:**  **P. SHANMUGA PANDIAN**
                      
    **Skills:**  **Python, SQL, EDA, Streamlit, Pandas, Power BI**                      
    """)
else:
    print("Created By was not found")