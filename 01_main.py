import streamlit as st

st.set_page_config(
    page_title="Laam Capital Dashboard"
)
st.title ("Trang chủ")
st.sidebar.success("Trade your best")

#page setup
map = st.Page(
    page= "02_Map.py",
    title="Laam Capital Map"
)

value = st.Page(
    page= "03_Value.py",
    title="Laam Capital Value"
)
st.subheader("Chào mừng bạn đến với Laam Capital Dashboard")
st.write("Đây là trang update các bộ lọc trong hệ thống đầu tư của mình. Bạn có thể vào đây để update realtime chart khi cần thiết. Chọn những thông tin bạn muốn xem ở **Navigation Bar**. ")
st.subheader("Tìm hiểu thêm về Laam Capital")
st.write("Room zalo thông tin thị trường: https://zalo.me/g/lkbdik522")
st.write("Kênh youtube: https://www.youtube.com/@Laamcapital")
st.subheader("Đầu tư cùng Laam Capital")
st.write("Tạo tài khoản forex: https://one.exnesstrack.org/a/l61iqtyq57")
st.write("Tạo tài khoản chứng khoán:")
st.image("qr.jpg", caption="Scan QR và làm theo hướng dẫn", use_column_width=True)
