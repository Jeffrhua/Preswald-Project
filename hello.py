from preswald import connect, get_df, text, table, query, plotly, text_input
import plotly.express as px
import pandas as pd

# Global variables:
data = "AirQualityData"

# Columns to drop
colsToDrop = ["NOx(GT)", "NO2(GT)", "O3(GT)", "SO2(GT)", "PM10", "Temperature", "Humidity", "Pressure", "WindSpeed", "WindDirection", "CO_NOx_Ratio", "NOx_NO2_Ratio", "Temp_Humidity_Index", "CO_MA3", "NO2_MA3", "O3_MA3", "DayOfWeek", "Hour"]

# Drop uneeded columns and set tables to the right data type
def parse_data(df):
    df = df.drop(columns=colsToDrop)
    df["DateTime"] = df["Date"] + " " + df["Time"]
    df = df.drop(columns=["Date", "Time"])
    
    for col in ["AirQualityIndex", "PM2.5", "CO(GT)"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    return df

def main():
    connect()
    
    # Post raw data
    text("# Air Quality Data Analysis")
    df = get_df(data)
    text("# Raw unfiltered data:")
    table(df)

    # Use text_input to let the user type a date
    selected_date = text_input("Enter a date (2024-01-01) - (2024-06-15):", default="2024-01-01")

    # Grab data for a selected day
    text(f"# Raw data values for `{selected_date}` before parsing")
    day_sql = f'SELECT * FROM {data} WHERE "Date" = \'{selected_date}\''
    filtered_df = query(day_sql, data)
    table(filtered_df)

    # Parse data, removing data points we are not concerned about (Only AQI, CO(GT), and PM2.5)
    filtered_df = parse_data(filtered_df)
    text(f"# Parsed data for `{selected_date}`")
    table(filtered_df)

    # AQI Plot
    fig = px.scatter(filtered_df, x="DateTime", y="AirQualityIndex", title=f"AQI on {selected_date}")
    plotly(fig)

    # CO(GT) Plot
    fig = px.scatter(filtered_df, x="DateTime", y="CO(GT)", title=f"CO(GT) on {selected_date}")
    plotly(fig)

    # PM2.5 Plot
    fig = px.scatter(filtered_df, x="DateTime", y="PM2.5", title=f"PM2.5 on {selected_date}")
    plotly(fig)

main()
