# Install necessary libraries
#pip install vnstock==0.2.9.2.3
#pip install openpyxl
#pip install adjustText
#pip install streamlitimport 
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
import tqdm




# Định nghĩa hàm chính cho trang
def main():
    st.title("Định giá tương đối và dòng tiền")
    st.markdown("Trang này thực hiện phân tích dữ liệu chứng khoán với tốc độ nhanh hơn.")

    # Danh sách chỉ số
    index_options = ['VN30', 'VNMID', 'VN100', 'VNSML', 'HNX30', 'VNXALL']
    index_name = st.selectbox("Chọn chỉ số", options=index_options, index=0)

    if st.button("Phân tích"):
        st.spinner("Đang tải dữ liệu và phân tích, vui lòng chờ...")

        # Thực hiện phân tích
        analyze_stock_data(index_name)


def analyze_stock_data(index_name):
    """Hàm thực hiện phân tích dữ liệu chứng khoán cho chỉ số được chọn."""
    st.write(f"Phân tích dữ liệu cho chỉ số: {index_name}")

    listing_df = listing_companies()
    ticker_list = listing_df.loc[listing_df[index_name] == True, 'ticker']

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")

    # Lấy dữ liệu khối lượng và P/E song song
    def get_stock_data(ticker):
        try:
            data = stock_historical_data(
                symbol=ticker, start_date=start_date, end_date=end_date, 
                resolution="1D", source='DNSE'
            )[["ticker", "volume"]]
            pe_data = stock_evaluation(symbol=ticker, period=1, time_window="D")[["ticker", "PE"]].iloc[[-1]]
            return data, pe_data
        except Exception:
            return None, None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results =list(tqdm.tqdm(executor.map(get_stock_data, ticker_list), total=len(ticker_list)))


    # Kết hợp dữ liệu
    df = pd.concat([result[0] for result in results if result[0] is not None], ignore_index=True)
    pe = pd.concat([result[1] for result in results if result[1] is not None], ignore_index=True)

    # Tính toán sự thay đổi khối lượng
    df_result = pd.DataFrame(columns=["ticker", "volume_change_percent"])
    for ticker in df["ticker"].unique():
        df_ticker = df[df["ticker"] == ticker]
        avg_volume_20 = df_ticker["volume"].rolling(window=20).mean().iloc[-1]
        avg_volume_50 = df_ticker["volume"].rolling(window=50).mean().iloc[-1]
        volume_change_percent = ((avg_volume_20 - avg_volume_50) / avg_volume_50) * 100 if avg_volume_50 != 0 else 0
        df_result = pd.concat([df_result, pd.DataFrame({"ticker": [ticker], "volume_change_percent": [volume_change_percent]})])

    # Phân tích Percentile
    df_result["volume_change_percentile"] = pd.qcut(df_result["volume_change_percent"], q=10, labels=False)
    pe["PE_percentile"] = pd.qcut(pe["PE"], q=10, labels=False)

    merged_df = pd.merge(pe, df_result, on="ticker")

    # Vẽ biểu đồ
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x="volume_change_percentile", y="PE_percentile", data=merged_df)

    texts = []
    for _, row in merged_df.iterrows():
        texts.append(plt.text(row["volume_change_percentile"], row["PE_percentile"], row["ticker"]))

    adjust_text(texts, arrowprops=dict(arrowstyle="->", color="red"))
    plt.axhline(y=4, color="g", linestyle="-")
    plt.axvline(x=5, color="g", linestyle="-")
    plt.axline([8, 8], [8, 10], color="g", linestyle="-")  # Đường xiên từ (8,8) đến (8,10)
    plt.axline((0, 4), (10, 10), color="blue", linestyle="--", label="y = 0.6x + 4")  # Đường
    plt.xlabel("Volume Change Percentile")
    plt.ylabel("PE Percentile")
    plt.title(f"Phân tích PE vs. Volume ({index_name})")
    st.pyplot(plt)

   
    


if __name__ == "__main__":
    main()
