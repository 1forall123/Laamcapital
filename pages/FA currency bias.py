import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def fetch_html(url, headers=None):
    """Lấy nội dung HTML từ một URL."""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Lỗi: {response.status_code}")
        return None

def parse_html(html):
    """Phân tích HTML bằng BeautifulSoup."""
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_table_data(soup, table_selector):
    """Trích xuất dữ liệu từ một bảng HTML."""
    table = soup.select_one(table_selector)
    if not table:
        st.warning("Không tìm thấy bảng!")
        return []

    data = []
    for row in table.find_all("tr"):
        cells = [cell.get_text(strip=True) for cell in row.find_all(["th", "td"])]
        data.append(cells)

    return data

def main():
    st.title("📊 Phân tích cơ bản FX")
    
    url = "https://fundamentaltrades.com/fundamental-bias/bias-scorecard/"
    headers = {"User-Agent": "Mozilla/5.0"}

    html = fetch_html(url, headers)
    if html:
        soup = parse_html(html)
        table_data = extract_table_data(soup, "table")  # Điều chỉnh selector nếu cần

        if table_data:
            # Chuyển dữ liệu thành DataFrame
            df = pd.DataFrame(table_data[1:], columns=table_data[0])
            
            # Hiển thị bảng trên Streamlit
            st.write("### Dữ liệu từ bảng:")
            st.dataframe(df)

            # Tải xuống file CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Tải xuống CSV", data=csv, file_name="bias_scorecard.csv", mime="text/csv")

if __name__ == "__main__":
    main()