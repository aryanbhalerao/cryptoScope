import requests
import datetime
import matplotlib as plt
import streamlit as st
import pandas as pd

def get_crypto_history(crypto_name):
    # Convert cryptocurrency name to CoinGecko ID
    search_url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(search_url)
    if response.status_code != 200:
        st.error("Failed to fetch data.")
        return None
    
    coins = response.json()
    crypto_id = None
    for coin in coins:
        if coin['name'].lower() == crypto_name.lower():
            crypto_id = coin['id']
            break
    
    if not crypto_id:
        st.error("Cryptocurrency not found!")
        return None
    
    # Fetch historical data
    history_url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days=30"
    response = requests.get(history_url)
    if response.status_code != 200:
        st.error("Failed to fetch historical data.")
        return None
    
    data = response.json()
    prices = data.get("prices", [])
    
    dates = [datetime.datetime.fromtimestamp(price[0] / 1000).strftime('%Y-%m-%d') for price in prices]
    values = [price[1] for price in prices]
    
    return dates, values

def main():
    st.title("Cryptocurrency Tracker")
    crypto_name = st.text_input("Enter cryptocurrency name:")
    
    if st.button("Get History"):
        result = get_crypto_history(crypto_name)
        if result:
            dates, values = result
            
            st.write(f"Historical prices for {crypto_name} (last 30 days):")
            df = pd.DataFrame({"Date": dates, "Price (USD)": values})
            df.index += 1
            
            # Visualization
            plt.figure(figsize=(10,5))
            plt.plot(dates, values, marker='o', linestyle='-', color='b')
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.title(f"Price History of {crypto_name}")
            plt.xticks(rotation=45)
            plt.grid()
            st.pyplot(plt)

            # Display data in four columns
            cols = st.columns(4)
            for i in range(len(df)):
                with cols[i % 4]:
                    st.write(f"{df.iloc[i]['Date']}: ${df.iloc[i]['Price (USD)']:.2f}")
            
if __name__ == "__main__":
    main()
