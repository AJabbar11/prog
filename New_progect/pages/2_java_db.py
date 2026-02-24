import streamlit as st
import time

# --- 1. إعدادات الصفحة والتصميم البلوري ---
st.set_page_config(page_title="محاكي جسر الربط JDBC المتكامل", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0f172a; color: white; }
    
    /* تصميم حاوية الجسر */
    .bridge-container {
        border: 2px dashed rgba(78, 204, 163, 0.5);
        border-radius: 20px;
        padding: 40px;
        background: rgba(255, 255, 255, 0.02);
        position: relative;
        margin: 20px 0;
    }
    
    /* أنيميشن نبضة البيانات */
    .signal {
        width: 15px; height: 15px;
        background: #00ff7f;
        border-radius: 50%;
        position: absolute;
        top: 50%;
        box-shadow: 0 0 15px #00ff7f;
        animation: flow 1.5s linear infinite;
    }
    
    @keyframes flow {
        0% { left: 10%; opacity: 0; }
        50% { opacity: 1; }
        100% { left: 85%; opacity: 0; }
    }
    
    .icon-box { font-size: 50px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌉 محاكي عمليات JDBC (إضافة، حذف، ترتيب)")

# --- 2. إدارة البيانات في القاعدة ---
if 'db_data' not in st.session_state:
    st.session_state.db_data = ["أحمد", "سارة", "زينة"]

# --- 3. واجهة التحكم ---
col_ctrl, col_bridge = st.columns([1.1, 1.4])

with col_ctrl:
    st.markdown('<div style="background:rgba(255,255,255,0.05); padding:20px; border-radius:15px;">', unsafe_allow_html=True)
    st.subheader("🛠️ لوحة تحكم الربط")
    
    connection_mode = st.radio("أسلوب البرمجة:", ["الأسلوب التقليدي (Main)", "أسلوب الدوال (Methods)"], horizontal=True)
    db_action = st.selectbox("نوع العملية المطلوبة:", ["إضافة (Insert)", "حذف (Delete)", "ترتيب (Sort)", "عرض (Select)"])
    
    # حقل إدخال القيمة (يختفي في حالة الترتيب والعرض)
    input_val = ""
    if db_action in ["إضافة (Insert)", "حذف (Delete)"]:
        label = "الاسم المراد إضافته:" if db_action == "إضافة (Insert)" else "الاسم المراد حذفه:"
        input_val = st.text_input(label, "علي")
    
    execute_btn = st.button("تفعيل الجسر وتنفيذ الكود 🚀")
    st.markdown('</div>', unsafe_allow_html=True)

with col_bridge:
    st.markdown('<div class="bridge-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 3, 1])
    with c1:
        st.markdown('<div class="icon-box">☕</div>', unsafe_allow_html=True)
        st.caption("Java Env")
    with c2:
        bridge_placeholder = st.empty()
        bridge_placeholder.markdown('<div style="height:4px; background:#333; margin-top:25px;"></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="icon-box">🗄️</div>', unsafe_allow_html=True)
        st.caption("Access DB")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # عرض الجدول
    st.write("📂 محتوى قاعدة البيانات الحالية:")
    st.table({"أسماء المستخدمين": st.session_state.db_data})

# --- 4. منطق التنفيذ والأنيميشن ---
if execute_btn:
    bridge_placeholder.markdown('<div class="signal"></div><div style="height:4px; background:#4ecca3; margin-top:25px;"></div>', unsafe_allow_html=True)
    
    with st.spinner("جاري الاتصال بالقاعدة..."):
        time.sleep(1.2)
        
        if db_action == "إضافة (Insert)":
            st.session_state.db_data.append(input_val)
            st.success(f"✅ تم تنفيذ الإضافة للقيمة: {input_val}")
        
        elif db_action == "حذف (Delete)":
            if input_val in st.session_state.db_data:
                st.session_state.db_data.remove(input_val)
                st.error(f"🗑️ تم حذف '{input_val}' من القاعدة.")
            else:
                st.warning("⚠️ الاسم غير موجود في القاعدة.")
        
        elif db_action == "ترتيب (Sort)":
            st.session_state.db_data.sort()
            st.info("⚖️ تم إعادة ترتيب البيانات أبجدياً.")
        
        elif db_action == "عرض (Select)":
            st.balloons()
            st.success("🔍 تم جلب كافة السجلات بنجاح.")

    time.sleep(1)
    bridge_placeholder.markdown('<div style="height:4px; background:#333; margin-top:25px;"></div>', unsafe_allow_html=True)
    st.rerun()

# --- 5. عرض الكود البرمجي المقابل ---
st.divider()
st.subheader("📝 كود الجافا المقابل (JDBC Code)")

if connection_mode == "الأسلوب التقليدي (Main)":
    if db_action == "إضافة (Insert)":
        code = f'st.executeUpdate("INSERT INTO Users VALUES (\'{input_val}\')");'
    elif db_action == "حذف (Delete)":
        code = f'st.executeUpdate("DELETE FROM Users WHERE name=\'{input_val}\'");'
    elif db_action == "ترتيب (Sort)":
        code = 'ResultSet rs = st.executeQuery("SELECT * FROM Users ORDER BY name ASC");'
    else:
        code = 'ResultSet rs = st.executeQuery("SELECT * FROM Users");'
else:
    # أسلوب الدوال
    if db_action == "إضافة (Insert)":
        code = f'public void addUser(String n) {{\n    st.executeUpdate("INSERT INTO Users VALUES (\'"+n+"\')");\n}}\n// Call:\naddUser("{input_val}");'
    elif db_action == "حذف (Delete)":
        code = f'public void deleteUser(String n) {{\n    st.executeUpdate("DELETE FROM Users WHERE name=\'"+n+"\'");\n}}\n// Call:\ndeleteUser("{input_val}");'
    elif db_action == "ترتيب (Sort)":
        code = 'public ResultSet getSorted() {\n    return st.executeQuery("SELECT * FROM Users ORDER BY name ASC");\n}'
    else:
        code = 'public ResultSet getAll() {\n    return st.executeQuery("SELECT * FROM Users");\n}'

st.code(code, language="java")

st.divider()
st.info("💡 لاحظ كيف يتغير كود الـ SQL (INSERT, DELETE, ORDER BY) بناءً على العملية المختارة، وكيف يتم تنظيم الكود عند اختيار 'أسلوب الدوال'.")