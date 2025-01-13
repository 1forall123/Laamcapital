# Install necessary libraries
#pip install vnstock==0.2.9.2.3
#pip install openpyxl
#pip install adjustText
#pip install streamlit

import streamlit as st
from vnstock import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
import concurrent.futures
from tqdm.notebook import tqdm

# Function to get ticker list based on index name
def get_ticker_list(index_name):
    indices = ['VN30', 'VN100', 'VNMID', 'VNSML', 'HNX30', 'VNXALL', 'VNCOND', 'VNCONS',
               'VNENE', 'VNFIN', 'VNHEAL', 'VNIND', 'VNIT', 'VNMAT', 'VNREAL', 'VNUTI']
    if index_name in indices:
        return listing_companies().loc[listing_companies()[index_name] == True]['ticker']
    return []

# Function to calculate RS rating for tickers
def calculate_rs_rating(ticker_list):
    RS = pd.DataFrame(columns=['ticker', 'rs'])
    for ticker in ticker_list:
        try:
            a = general_rating(ticker)['rsRating']
            RS = pd.concat([RS, pd.DataFrame({'ticker': [ticker], 'rs': [a.values[0]]})], ignore_index=True)
        except:
            pass
    return RS

# Function to calculate volume change
def calculate_volume_change(ticker_list, start_date_str, end_date_str):
    results = []
    for ticker in ticker_list:
        try:
            vol = stock_historical_data(
                symbol=ticker,
                start_date=start_date_str,
                end_date=end_date_str,
                resolution="1D",
                type="stock",
                beautify=True,
                decor=False,
                source='DNSE'
            )[['ticker', 'volume']]
            vol['MA20'] = vol['volume'].rolling(window=20).mean()
            vol['MA50'] = vol['volume'].rolling(window=50).mean()
            vol['diff_MA20_MA50_percent'] = ((vol['MA20'] - vol['MA50']) / vol['MA50']) * 100
            if not vol['diff_MA20_MA50_percent'].empty:
                latest_diff = vol['diff_MA20_MA50_percent'].iloc[-1]
                results.append({'ticker': ticker, 'diff_MA20_MA50_percent': latest_diff})
        except:
            pass
    return pd.DataFrame(results)

# Function to plot RS vs volume change with categorized zones
def plot_rs_vs_volume_change(merged_df):
    plt.figure(figsize=(15, 10))

    # Define zones based on conditions
    strong = merged_df[(merged_df['diff_MA20_MA50_percent'] > 0) & (merged_df['rs'] >= 3.5)]
    in_flow = merged_df[(merged_df['diff_MA20_MA50_percent'] <= 0) & (merged_df['rs'] >= 3.5)]
    watch = merged_df[(merged_df['rs'] >= 3) & ~merged_df.index.isin(in_flow.index) & ~merged_df.index.isin(strong.index)]
    skip = merged_df[merged_df['rs'] < 2]
    neutral = merged_df[~merged_df.index.isin(in_flow.index) & ~merged_df.index.isin(strong.index) &
                        ~merged_df.index.isin(watch.index) & ~merged_df.index.isin(skip.index)]

    # Plot each zone with different colors
    sns.scatterplot(x='rs', y='diff_MA20_MA50_percent', data=in_flow, color='green', label='Dòng tiền vào', s=100)
    sns.scatterplot(x='rs', y='diff_MA20_MA50_percent', data=strong, color='purple', label='Cổ phiếu mạnh', s=100)
    sns.scatterplot(x='rs', y='diff_MA20_MA50_percent', data=watch, color='orange', label='Vùng quan sát', s=100)
    sns.scatterplot(x='rs', y='diff_MA20_MA50_percent', data=skip, color='red', label='Bỏ qua', s=50)
    sns.scatterplot(x='rs', y='diff_MA20_MA50_percent', data=neutral, color='blue', label='Trung lập', s=50, alpha=0.6)

    # Annotate the points with ticker symbols
    for _, row in merged_df.iterrows():
        plt.annotate(
            row['ticker'],
            (row['rs'], row['diff_MA20_MA50_percent']),
            textcoords="offset points",
            xytext=(5, 5),
            ha='center',
            fontsize=8,
            color='black',
        )

    # Display plot details
    plt.xlabel('Hướng giá')
    plt.ylabel('Dòng tiền')
    plt.title('Map')
    plt.grid(False)
    st.pyplot(plt)
# Streamlit app
def main():
    st.title("Laam Capital Map")
    indices = ['VN30', 'VN100', 'VNMID', 'VNSML', 'HNX30', 'VNXALL', 'VNCOND', 'VNCONS',
               'VNENE', 'VNFIN', 'VNHEAL', 'VNIND', 'VNIT', 'VNMAT', 'VNREAL', 'VNUTI']
    index_name = st.selectbox("Chọn chỉ số", indices)
    
    if st.button("Phân tích"):
        st.write(f"Chờ tí nhé: {index_name}")
        ticker_list = get_ticker_list(index_name)
        rs_df = calculate_rs_rating(ticker_list)
        today = datetime.today()
        start_date = today - timedelta(days=100)
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = today.strftime('%Y-%m-%d')
        vol_diff_df = calculate_volume_change(ticker_list, start_date_str, end_date_str)
        merged_df = pd.merge(vol_diff_df, rs_df, on='ticker', how='inner').sort_values('diff_MA20_MA50_percent', ascending=False)
        plot_rs_vs_volume_change(merged_df)
        

if __name__ == "__main__":
    main()
