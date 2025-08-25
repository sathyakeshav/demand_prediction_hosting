import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set the page configuration for a centered layout
st.set_page_config(page_title="📊 Demand Data Forecaster", layout="centered")

# --- Introduction Section ---
st.header("🔑 Unlock Your Data's Future")
st.markdown("""
Ready to predict what's next for your business? This tool makes it simple to forecast demand using your own historical data.

Just upload a `.csv` file, and watch as our powerful backend service analyzes your time series data and generates a beautiful, insightful plot.

Stop guessing and start predicting. Get a clear view of your future demand in just a few clicks.
""")

st.image("https://placehold.co/600x400/808080/FFFFFF?text=Data+Forecasting+Chart")
st.markdown("---") # Add a horizontal line to separate the sections.

# --- Application Section (Scroll-down content) ---
st.title("📈 Demand Data Forecaster")
st.markdown("Upload a `.csv` file with two columns named `date` and `demand`.")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    st.success("File uploaded successfully!")

    if st.button("📤 Submit to Lambda"):
        with st.spinner("Calling AWS Lambda..."):
            api_url = "https://db4z7ymxuf.execute-api.us-east-1.amazonaws.com/default/forecast" # Replace with your Prophet API
            try:
                response = requests.post(
                    api_url,
                    data=uploaded_file.getvalue(),
                    headers={"Content-Type": "thttps://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/prophet?tab=aliasesext/csv"}
                )

                if response.status_code == 200:
                    result = response.json()
                    df = pd.DataFrame({
                        "date": pd.to_datetime(result["date"]),
                        "demand": result["forecast"]
                    })
                    
                    # Create the plot
                    st.subheader("📊 Demand Time Series Plot")
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(df["date"], df["demand"], color="tab:blue", label="Forecast")

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

st.markdown("---")
st.header("For Developers 👨‍")
st.markdown("Are you a developer? You can use this service directly in your applications!")
st.link_button("Access the API on RapidAPI", "https://rapidapi.com/info-TdHyg7Xv9/api/prophet-demand-forecasting/playground/apiendpoint_de0cdfdb-b17c-43e6-8232-0314c9c60db8")
