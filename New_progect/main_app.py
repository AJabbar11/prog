import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة علوم الحاسوب", layout="wide")

# 2. كود CSS المحسن (أضفت تنسيقاً خاصاً لـ st.container)
st.markdown("""
    <style>
    /* الخلفية المتحركة */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* العنوان الرئيسي */
    .header-text {
        text-align: center;
        color: white;
        font-size: 50px;
        font-weight: bold;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        margin-bottom: 50px;
    }

    /* تنسيق الحاوية (البوكس) */
    [data-testid="stVerticalBlock"] > div:has(div.card-content) {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        text-align: center !important;
        transition: 0.3s !important;
    }

    /* تأثير الحرك عند المرور بالماوس */
    [data-testid="stVerticalBlock"] > div:has(div.card-content):hover {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.3) !important;
    }

    /* تنسيق النصوص والأزرار داخل البوكس */
    .card-title {
        color: white;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 15px;
        display: block;
    }
    
    .stButton > button {
        background-color: white !important;
        color: #e73c7e !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. العنوان الرئيسي
st.markdown('<div class="header-text">المرحلة الثانية - علوم حاسوب</div>', unsafe_allow_html=True)

# 4. توزيع البوكسات
col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        # كلاس فارغ لتمكين CSS من التعرف على هذا الكونتينر
        st.markdown('<div class="card-content"></div>', unsafe_allow_html=True)
        st.markdown('<span class="card-title">🗄️<br>قواعد البيانات</span>', unsafe_allow_html=True)
        if st.button("دخول الكورس", key="db"):
            st.switch_page("pages/1_database.py")

with col2:
    with st.container():
        st.markdown('<div class="card-content"></div>', unsafe_allow_html=True)
        st.markdown('<span class="card-title">☕<br>ربط الجافا بالقواعد</span>', unsafe_allow_html=True)
        if st.button("دخول الكورس", key="java"):
            st.switch_page("pages/2_java_db.py")

with col3:
    with st.container():
        st.markdown('<div class="card-content"></div>', unsafe_allow_html=True)
        st.markdown('<span class="card-title">🏗️<br>هياكل البيانات</span>', unsafe_allow_html=True)
        if st.button("دخول الكورس", key="ds"):
            st.switch_page("pages/3_data_structures.py")