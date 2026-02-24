import streamlit as st
import pandas as pd
import time

# --- 1. إعدادات الصفحة والتصميم (مطابق للرئيسية) ---
st.set_page_config(page_title="محاكي جداول Access", layout="wide")

st.markdown("""
    <style>
    /* الخلفية الانسيابية المتحركة (نفس الرئيسية) */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* تصميم إطار برنامج Access */
    .access-ui {
        background-color: #ffffff;
        border-top: 40px solid #a4373a; /* شريط Access العلوي */
        border-radius: 10px;
        padding: 20px;
        color: #333;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .access-header {
        color: #a4373a;
        font-weight: bold;
        border-bottom: 2px solid #eee;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🗄️ محاكي إدارة جداول Microsoft Access")

# --- 2. إدارة بيانات الجدول ---
if 'access_table' not in st.session_state:
    st.session_state.access_table = pd.DataFrame([
        {"المعرف": 1, "الاسم": "أحمد", "التخصص": "حاسبات"},
        {"المعرف": 2, "الاسم": "سارة", "التخصص": "برمجيات"}
    ])

# --- 3. شرح مبسط للتحكم ---
st.info("""
**💡 كيفية التحكم في الجدول:**
1. **الإضافة:** قم بتعبئة الحقول في الأسفل لإضافة سجل جديد مباشرة للجدول.
2. **الحذف:** اختر رقم المعرف المراد مسحه من قاعدة البيانات.
3. **الترتيب:** استخدم زر الترتيب لتنظيم الأسماء أبجدياً داخل ملف الـ Access.
""")

# --- 4. واجهة المحاكاة ---
col_actions, col_display = st.columns([1, 1.5])

with col_actions:
    st.markdown("### 🛠️ لوحة العمليات")
    
    tab1, tab2, tab3 = st.tabs(["➕ إضافة", "🗑️ حذف", "🔃 ترتيب"])
    
    with tab1:
        new_id = st.number_input("المعرف (ID):", min_value=3, step=1)
        new_name = st.text_input("الاسم:")
        new_major = st.text_input("التخصص:")
        add_btn = st.button("إضافة سجل جديد ✅")

    with tab2:
        delete_id = st.number_input("أدخل ID السجل للحذف:", min_value=1, step=1)
        del_btn = st.button("حذف السجل ❌")

    with tab3:
        st.write("ترتيب الجدول حسب الاسم:")
        sort_btn = st.button("ترتيب أبجدي 🔃")

with col_display:
    st.markdown('<div class="access-ui">', unsafe_allow_html=True)
    st.markdown('<div class="access-header">📄 Table: Students_Database</div>', unsafe_allow_html=True)
    
    table_area = st.empty()
    table_area.dataframe(st.session_state.access_table, use_container_width=True, hide_index=True)
    
    # تنفيذ العمليات
    if add_btn:
        new_data = {"المعرف": new_id, "الاسم": new_name, "التخصص": new_major}
        st.session_state.access_table = pd.concat([st.session_state.access_table, pd.DataFrame([new_data])], ignore_index=True)
        st.success("تمت الإضافة بنجاح!")
        time.sleep(0.5)
        st.rerun()

    if del_btn:
        st.session_state.access_table = st.session_state.access_table[st.session_state.access_table["المعرف"] != delete_id]
        st.warning(f"تم حذف السجل رقم {delete_id}")
        time.sleep(0.5)
        st.rerun()

    if sort_btn:
        st.session_state.access_table = st.session_state.access_table.sort_values(by="الاسم")
        st.info("تم ترتيب الجدول!")
        time.sleep(0.5)
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. شرح مرئي لمكونات Access ---
st.divider()


st.markdown("""
<div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; direction: rtl; text-align: right;">
    <h3>📌 مفاهيم أساسية في Access:</h3>
    <ul>
        <li><b>الحقول (Fields):</b> هي الأعمدة (مثل الاسم، العمر) وتحدد نوع البيانات.</li>
        <li><b>السجلات (Records):</b> هي الصفوف، وكل صف يمثل بيانات شخص واحد.</li>
        <li><b>المفتاح الأساسي (Primary Key):</b> هو رقم فريد (مثل ID) لا يتكرر لضمان عدم اختلاط البيانات.</li>
    </ul>
</div>
""", unsafe_allow_html=True)



# زر العودة للرئيسية
if st.sidebar.button("🏠 العودة للرئيسية"):
    st.switch_page("main_app.py")