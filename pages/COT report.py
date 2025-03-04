import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from cot_reports import cot_year

# ======================================
# 1) Danh mục COT (đã sửa tên Energy)
# ======================================
def get_cot_report():
    return {
        "Forex": [
            "EURO FX - CHICAGO MERCANTILE EXCHANGE",
            "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE",
            "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE",
            "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
            "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
            "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE",
            "NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE",
            "USD INDEX - ICE FUTURES U.S.",
        ],
        "Indices": {
            "Major Indices": [
                "DJAI Consolidated - CHICAGO BOARD OF TRADE",
                "DJIA x $5 - CHICAGO BOARD OF TRADE",
                "S&P 500 Consolidated - CHICAGO MERCANTILE EXCHANGE",
                "E-MINI S&P 500 - CHICAGO MERCANTILE EXCHANGE",
                "MICRO E-MINI S&P 500 INDEX - CHICAGO MERCANTILE EXCHANGE",
                "NASDAQ-100 Consolidated - CHICAGO MERCANTILE EXCHANGE",
                "NASDAQ MINI - CHICAGO MERCANTILE EXCHANGE",
                "MICRO E-MINI NASDAQ-100 INDEX - CHICAGO MERCANTILE EXCHANGE",
                "RUSSELL E-MINI - CHICAGO MERCANTILE EXCHANGE",
                "MICRO E-MINI RUSSELL 2000 INDX - CHICAGO MERCANTILE EXCHANGE",
            ],
            "Sector Indices": [
                "E-MINI S&P CONSU STAPLES INDEX - CHICAGO MERCANTILE EXCHANGE",
                "E-MINI S&P ENERGY INDEX - CHICAGO MERCANTILE EXCHANGE",
                "E-MINI S&P FINANCIAL INDEX - CHICAGO MERCANTILE EXCHANGE",
                "E-MINI S&P MATERIALS INDEX - CHICAGO MERCANTILE EXCHANGE",
                "E-MINI S&P TECHNOLOGY INDEX - CHICAGO MERCANTILE EXCHANGE",
                "E-MINI S&P UTILITIES INDEX - CHICAGO MERCANTILE EXCHANGE",
                "E-MINI S&P COMMUNICATION INDEX - CHICAGO MERCANTILE EXCHANGE"
            ],
            "Volatility & Global Indices": [
                "S&P 500 ANNUAL DIVIDEND INDEX - CHICAGO MERCANTILE EXCHANGE",
                "S&P 500 QUARTERLY DIVIDEND IND - CHICAGO MERCANTILE EXCHANGE",
                "NIKKEI STOCK AVERAGE - CHICAGO MERCANTILE EXCHANGE",
                "NIKKEI STOCK AVERAGE YEN DENOM - CHICAGO MERCANTILE EXCHANGE",
                "MSCI EAFE - ICE FUTURES U.S.",
                "MSCI EM INDEX - ICE FUTURES U.S.",
                "VIX FUTURES - CBOE FUTURES EXCHANGE"
            ]
        },
        "Commodities": {
            "Metals": [
                "GOLD - COMMODITY EXCHANGE INC.",
                "SILVER - COMMODITY EXCHANGE INC.",
                "COMEX COPPER - COMMODITY EXCHANGE INC.",
                "PLATINUM - NEW YORK MERCANTILE EXCHANGE",
                "PALLADIUM - NEW YORK MERCANTILE EXCHANGE",
                "ALUMINUM - COMMODITY EXCHANGE INC.",
                "LITHIUM HYDROXIDE - COMMODITY EXCHANGE INC.",
                "COBALT - COMMODITY EXCHANGE INC."
            ],
            "Energy": [
                "CRUDE OIL, LIGHT SWEET-WTI - ICE FUTURES EUROPE",
                "ICE BRENT CRUDE OIL - ICE FUTURES EUROPE",
                "NATURAL GAS - NEW YORK MERCANTILE EXCHANGE",
                "RBOB GASOLINE - NEW YORK MERCANTILE EXCHANGE",
                "HEATING OIL - NEW YORK MERCANTILE EXCHANGE"
            ],
            "Grains & Oilseeds": [
                "WHEAT - CHICAGO BOARD OF TRADE",
                "CORN - CHICAGO BOARD OF TRADE",
                "SOYBEANS - CHICAGO BOARD OF TRADE",
                "OATS - CHICAGO BOARD OF TRADE",
                "ROUGH RICE - CHICAGO BOARD OF TRADE",
                "SOYBEAN MEAL - CHICAGO BOARD OF TRADE",
                "SOYBEAN OIL - CHICAGO BOARD OF TRADE"
            ],
            "Livestock": [
                "LIVE CATTLE - CHICAGO MERCANTILE EXCHANGE",
                "LEAN HOGS - CHICAGO MERCANTILE EXCHANGE",
                "FEEDER CATTLE - CHICAGO MERCANTILE EXCHANGE"
            ],
            "Soft Commodities": [
                "ICE COCOA - ICE FUTURES U.S.",
                "ICE COFFEE C - ICE FUTURES U.S.",
                "ICE COTTON NO. 2 - ICE FUTURES U.S.",
                "ICE ORANGE JUICE - ICE FUTURES U.S.",
                "ICE SUGAR NO. 11 - ICE FUTURES U.S."
            ]
        },
        "Bonds & Treasury": [
            "UST BOND - CHICAGO BOARD OF TRADE",
            "ULTRA UST BOND - CHICAGO BOARD OF TRADE",
            "UST 2Y NOTE - CHICAGO BOARD OF TRADE",
            "UST 5Y NOTE - CHICAGO BOARD OF TRADE",
            "UST 10Y NOTE - CHICAGO BOARD OF TRADE",
            "ULTRA UST 10Y - CHICAGO BOARD OF TRADE",
            "MICRO 10 YEAR YIELD - CHICAGO BOARD OF TRADE"
        ],
        "Interest Rates": [
            "FED FUNDS - CHICAGO BOARD OF TRADE",
            "SOFR-3M - CHICAGO MERCANTILE EXCHANGE",
            "SOFR-1M - CHICAGO MERCANTILE EXCHANGE",
            "EURO SHORT TERM RATE - CHICAGO MERCANTILE EXCHANGE",
            "2 YEAR ERIS SOFR SWAP - CHICAGO BOARD OF TRADE",
            "5 YEAR ERIS SOFR SWAP - CHICAGO BOARD OF TRADE",
            "10 YEAR ERIS SOFR SWAP - CHICAGO BOARD OF TRADE"
        ]
    }

# ======================================
# 2) Load dữ liệu (có cache)
# ======================================
@st.cache_data
def load_cot_data(year, report_type):
    df = cot_year(year=year, cot_report_type=report_type)
    df["Report_Date"] = pd.to_datetime(
        df.get("Report_Date_as_YYYY_MM_DD", df.get("As of Date in Form YYYY-MM-DD")),
        errors='coerce'
    )
    return df

# ======================================
# 3) Tính toán Long/Short Ratio + Net
# ======================================
def calculate_summary(df, contracts):
    """
    Trả về DataFrame có:
      - Full Contract
      - Short Name (rút gọn)
      - Report Date
      - Long Positions, Short Positions
      - Long %, Short %
      - Net Position
    """
    summary_data = []
    for contract in contracts:
        df_c = df[df["Market and Exchange Names"] == contract]
        if not df_c.empty:
            df_c = df_c.sort_values("Report_Date", ascending=False)
            latest_row = df_c.iloc[0]

            long_val = latest_row["Noncommercial Positions-Long (All)"]
            short_val = latest_row["Noncommercial Positions-Short (All)"]
            total = long_val + short_val if (long_val + short_val) != 0 else 1

            net_pos = long_val - short_val
            # Rút gọn tên
            short_name = contract.split(" - ")[0]

            summary_data.append({
                "Full Contract": contract,
                "Short Name": short_name,
                "Report Date": latest_row["Report_Date"].date() if pd.notnull(latest_row["Report_Date"]) else None,
                "Long Positions": long_val,
                "Short Positions": short_val,
                "Long %": round((long_val / total)*100, 2),
                "Short %": round((short_val / total)*100, 2),
                "Net Position": net_pos
            })

    return pd.DataFrame(summary_data)

# ======================================
# 4) Sinh “Tín hiệu giao dịch” (ví dụ)
# ======================================
def generate_trading_signals(summary_df):
    """
    Logic ví dụ:
      - If Long% > 60 => Bullish
      - If Short% > 60 => Bearish
      - Otherwise => Neutral
    """
    signals = []
    for _, row in summary_df.iterrows():
        if row["Long %"] > 60:
            signal = "Bullish"
        elif row["Short %"] > 60:
            signal = "Bearish"
        else:
            signal = "Neutral"
        signals.append(signal)

    summary_df["Signal"] = signals
    return summary_df

# ======================================
# 5) Plot Biểu đồ Tổng hợp (stacked bar)
# ======================================
def plot_summary_bar(summary_df):
    """
    Dùng "Short Name" làm index để biểu diễn cho gọn.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    # Copy ra để thao tác
    plot_df = summary_df.copy()
    plot_df.set_index("Short Name", inplace=True)

    plot_df[["Long %", "Short %"]].plot(kind="bar", stacked=True, ax=ax, color=["green", "red"])
    plt.title("Long/Short Ratio (Noncommercial) - Latest")
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Position")
    st.pyplot(fig)

# ======================================
# 6) Plot Biểu đồ chi tiết theo thời gian
# ======================================
def plot_detailed_timeseries(df, summary_df):
    """
    Vẽ chart cho từng 'Full Contract' nhưng
    tiêu đề hiển thị tên rút gọn 'Short Name'.
    """
    for _, row in summary_df.iterrows():
        full_contract = row["Full Contract"]
        short_name = row["Short Name"]

        df_c = df[df["Market and Exchange Names"] == full_contract].copy()
        if not df_c.empty:
            df_c = df_c.sort_values("Report_Date")

            df_c["Net Position"] = (
                df_c["Noncommercial Positions-Long (All)"] 
                - df_c["Noncommercial Positions-Short (All)"]
            )
            df_c["Long/Short Ratio"] = df_c["Noncommercial Positions-Long (All)"] / (
                df_c["Noncommercial Positions-Short (All)"].replace({0: 1})
            )

            fig, ax1 = plt.subplots(figsize=(10, 4))
            ax2 = ax1.twinx()

            ax1.plot(df_c["Report_Date"], df_c["Net Position"], label="Net Pos", color="blue")
            ax2.plot(df_c["Report_Date"], df_c["Long/Short Ratio"], label="L/S Ratio", color="red", linestyle="--")

            ax1.set_title(f"{short_name} - Net Position & L/S Ratio")
            ax1.set_xlabel("Report Date")
            ax1.set_ylabel("Net Position", color="blue")
            ax2.set_ylabel("Long/Short Ratio", color="red")
            ax1.legend(loc="upper left")
            ax2.legend(loc="upper right")

            plt.xticks(rotation=45)
            plt.grid()
            st.pyplot(fig)
        else:
            st.warning(f"⚠️ Không có dữ liệu cho {full_contract}")

# ======================================
# 7) Main App
# ======================================
def main():
    st.title("COT Report Viewer")

    # Sidebar select
    year = st.sidebar.selectbox("Chọn năm", list(range(2000, 2026)), index=24)
    report_type = st.sidebar.selectbox("Chọn loại báo cáo", ["legacy_fut", "legacy_futopt", "disaggregated_fut", "disaggregated_futopt"])

    cot_dict = get_cot_report()
    category = st.sidebar.selectbox("Chọn danh mục", list(cot_dict.keys()))

    if isinstance(cot_dict[category], dict):
        sub_category = st.sidebar.selectbox("Chọn tiểu danh mục", list(cot_dict[category].keys()))
        contracts = cot_dict[category][sub_category]
    else:
        contracts = cot_dict[category]

    # Load data
    df_cot = load_cot_data(year, report_type)
    if df_cot is None or df_cot.empty:
        st.error("❌ Không tìm thấy dữ liệu COT!")
        return

    # Tính summary
    summary_df = calculate_summary(df_cot, contracts)
    if summary_df.empty:
        st.error("❌ Không có dữ liệu cho hợp đồng trong danh mục này!")
        return

    # Sinh tín hiệu
    summary_df = generate_trading_signals(summary_df)

    # Tạo 2 tab
    tab_summary, tab_detail = st.tabs(["Tổng hợp", "Biểu đồ chi tiết"])

    with tab_summary:
        # Bảng tín hiệu (Long%, Short%, Net, Signal)
        st.subheader("Bảng Tổng Hợp & Tín Hiệu Giao Dịch")
        st.dataframe(summary_df[[
            "Short Name", "Report Date", "Long %", "Short %", "Net Position", "Signal"
        ]])

        # Biểu đồ stacked bar (dùng tên rút gọn)
        st.subheader("Biểu Đồ Long/Short Ratio (Noncommercial)")
        plot_summary_bar(summary_df)

    with tab_detail:
        st.subheader("Biểu đồ chi tiết (theo thời gian)")
        plot_detailed_timeseries(df_cot, summary_df)


if __name__ == "__main__":
    main()
