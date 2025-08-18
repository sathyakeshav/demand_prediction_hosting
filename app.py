import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(page_title="📊 Demand Data Visualizer", layout="centered")

st.title("📈 Demand Data Visualizer")
st.markdown("Upload a `.csv` file and view the demand time series plot.")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    st.success("File uploaded successfully!")

    if st.button("📤 Submit to Lambda"):
        with st.spinner("Calling AWS Lambda..."):
            api_url = "https://db4z7ymxuf.execute-api.us-east-1.amazonaws.com/default/forecast"  # Replace this your prophet api
            #api_url = "https://prophet-demand-forecasting.p.rapidapi.com/default/forecast"  # Replace this your prophet api
            try:
                response = requests.post(
                    api_url,
                    data=uploaded_file.getvalue(),
                    headers={"Content-Type": "thttps://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/prophet?tab=aliasesext/csv"}
                    #headers={
                    #    "X-RapidAPI-Key": "cdad1316demsha6d35161c3ecb21p1d666ajsn8b34a476bf5a",
                    #   "X-RapidAPI-Host": "prophet-demand-forecasting.p.rapidapi.com",
                    #   "Content-Type": "text/csv"}
                )

                if response.status_code == 200:
                    #st.write("Raw Lambda Response:", response.text) # ADD THIS LINE
                    result = response.json()
                    df = pd.DataFrame({
                        "date": pd.to_datetime(result["date"]),
                        "demand": result["forecast"]
                    })
                    df = df.rename(columns={"forecast": "demand"}) # ADD THIS LINE IF YOU WANT TO PLOT AS 'DEMAND'
                    st.subheader("📊 Demand Time Series Plot") # This subheader might also be renamed "Forecast Plot"
                    fig, ax = plt.subplots(figsize=(10, 5))
                    # ax.plot(df["date"], df["demand"], color="tab:blue", label="Demand") # This line now works as 'demand' column exists
                    ax.plot(df["date"], df["demand"], color="tab:blue", label="Forecast") # OR change label to 'Forecast'

                    # Format x-axis for better date visibility
                    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()

                    ax.set_xlabel("Date")
                    ax.set_ylabel("Demand")
                    ax.set_title("Demand Over Time")
                    ax.grid(True)

                    st.pyplot(fig)
                else:
                    st.error(f"Lambda returned {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"Error calling Lambda: {e}")
