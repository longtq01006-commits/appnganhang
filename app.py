import numpy as np
import pandas as pd
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(page_title="Tính Lãi Gửi Tiết Kiệm", page_icon="💰")

st.title("💰 Công Cụ Tính Lãi Gửi Tiết Kiệm")
st.write(
    "So sánh hiệu quả giữa **Lãi đơn** và **Lãi kép** theo số tiền và thời gian gửi."
)

# Tạo các ô nhập liệu ở thanh bên (Sidebar)
st.sidebar.header("📥 Nhập thông tin tiền gửi")

principal = st.sidebar.number_input(
    "Số tiền gửi ban đầu (VNĐ):",
    min_value=100000,
    value=100000000,
    step=1000000,
    format="%d",
)

months = st.sidebar.number_input(
    "Số tháng gửi:", min_value=1, max_value=600, value=12, step=1
)

annual_rate = st.sidebar.number_input(
    "Lãi suất hàng năm (%/năm):",
    min_value=0.1,
    max_value=50.0,
    value=6.0,
    step=0.1,
)

# Chuyển đổi lãi suất năm sang lãi suất tháng
monthly_rate = (annual_rate / 100) / 12

# 1. Tính Lãi Đơn
simple_interest = principal * monthly_rate * months
simple_total = principal + simple_interest

# 2. Tính Lãi Kép (Lãi nhập gốc hàng tháng)
compound_total = principal * ((1 + monthly_rate) ** months)
compound_interest = compound_total - principal

# Hiển thị kết quả tổng quan
st.subheader("📊 Kết quả tổng quan")

col1, col2 = st.columns(2)

with col1:
    st.info("### 🟢 Lãi Đơn")
    st.metric("Tiền lãi nhận được", f"{simple_interest:,.0f} VNĐ")
    st.metric("Tổng tiền thu về", f"{simple_total:,.0f} VNĐ")

with col2:
    st.success("### 🔵 Lãi Kép (Nhập gốc hàng tháng)")
    st.metric("Tiền lãi nhận được", f"{compound_interest:,.0f} VNĐ")
    st.metric(
        "Tổng tiền thu về",
        f"{compound_total:,.0f} VNĐ",
        delta=f"+{compound_interest - simple_interest:,.0f} VNĐ so với lãi đơn",
    )

# Bảng và Đồ thị tăng trưởng theo từng tháng
st.subheader("📈 Biểu đồ tăng trưởng tài sản theo thời gian")

months_array = np.arange(0, months + 1)
simple_growth = principal + (principal * monthly_rate * months_array)
compound_growth = principal * ((1 + monthly_rate) ** months_array)

# Tạo DataFrame lưu trữ tiến trình
df = pd.DataFrame(
    {
        "Tháng": months_array,
        "Lãi Đơn (VNĐ)": simple_growth,
        "Lãi Kép (VNĐ)": compound_growth,
    }
).set_index("Tháng")

# Vẽ đồ thị đường
st.line_chart(df)

# Cho phép xem chi tiết dữ liệu bảng
with st.expander("📄 Xem chi tiết bảng dòng tiền theo từng tháng"):
    st.dataframe(
        df.style.format(
            {"Lãi Đơn (VNĐ)": "{:,.0f}", "Lãi Kép (VNĐ)": "{:,.0f}"}
        )
    )
