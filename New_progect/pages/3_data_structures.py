import streamlit as st
import time

# --- 1. إعدادات الصفحة والتصميم البلوري ---
st.set_page_config(page_title="محاكي هياكل البيانات - مستويين", layout="wide")

st.markdown("""
    <style>
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
    .glass-container {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    .data-node {
        width: 80px; height: 80px;
        background: rgba(0, 210, 255, 0.2);
        border: 2px solid #00d2ff;
        border-radius: 12px;
        display: flex; justify-content: center; align-items: center;
        color: white; font-size: 22px; font-weight: bold;
        transition: all 0.4s ease;
    }
    .processing-node {
        background: rgba(0, 255, 127, 0.4) !important;
        border-color: #00ff7f !important;
        transform: scale(1.1) translateY(-10px);
        box-shadow: 0 0 25px #00ff7f;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ محاكي هياكل البيانات (الأسلوب التقليدي vs الدوال)")

# --- 2. إدارة البيانات ---
if 'array_list' not in st.session_state:
    st.session_state.array_list = ["50", "10", "40", "20"]

# --- 3. الواجهة الرسومية ---
col_editor, col_visual = st.columns([1.2, 1.2])

with col_editor:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.subheader("📝 Java Code Viewer")
    
    # اختيار الأسلوب البرمجي
    code_style = st.radio("اختر أسلوب البرمجة:", ["الأسلوب التقليدي (بدون دوال)", "أسلوب الدوال (Methods)"], horizontal=True)
    
    # اختيار العملية
    op = st.selectbox("اختر العملية:", ["إضافة (Insert)", "حذف (Delete)", "بحث (Search)", "ترتيب (Sort)"])
    
    # إدخال القيمة
    if op != "ترتيب (Sort)":
        input_val = st.text_input("أدخل القيمة أو الموقع:", "30")
    else:
        input_val = ""

    # منطق عرض الكود بناءً على الأسلوب
    if code_style == "الأسلوب التقليدي (بدون دوال)":
        if op == "إضافة (Insert)":
            final_code = f"// الكود داخل الـ main مباشرة\nlist.add(\"{input_val}\");"
        elif op == "حذف (Delete)":
            final_code = f"int index = {input_val if input_val.isdigit() else 0};\nlist.remove(index);"
        elif op == "بحث (Search)":
            final_code = f"for(int i=0; i<list.size(); i++) {{\n    if(list.get(i).equals(\"{input_val}\")) {{\n        System.out.println(\"Found\");\n    }}\n}}"
        else:
            final_code = "for(int i=0; i<n-1; i++) {\n    for(int j=0; j<n-i-1; j++) {\n        if(arr[j] > arr[j+1]) { // Swap }\n    }\n}"
    else:
        # أسلوب الدوال
        if op == "إضافة (Insert)":
            final_code = f"public void addElement(String val) {{\n    list.add(val);\n}}\n\n// الاستدعاء:\naddElement(\"{input_val}\");"
        elif op == "حذف (Delete)":
            final_code = f"public void removeAtIndex(int i) {{\n    list.remove(i);\n}}\n\n// الاستدعاء:\nremoveAtIndex({input_val if input_val.isdigit() else 0});"
        elif op == "بحث (Search)":
            final_code = f"public int findElement(String val) {{\n    return list.indexOf(val);\n}}\n\n// الاستدعاء:\nfindElement(\"{input_val}\");"
        else:
            final_code = "public void sortArray() {\n    Collections.sort(list);\n}\n\n// الاستدعاء:\nsortArray();"

    st.code(final_code, language="java")
    execute_btn = st.button("تنفيذ المحاكاة 🚀")
    st.markdown('</div>', unsafe_allow_html=True)

with col_visual:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.subheader("📺 المحاكاة الحية")
    
    viz_placeholder = st.empty()
    status_log = st.empty()

    def render_visuals(highlights=[]):
        if len(st.session_state.array_list) > 0:
            cols = viz_placeholder.columns(len(st.session_state.array_list))
            for i, val in enumerate(st.session_state.array_list):
                with cols[i]:
                    style_class = "processing-node" if i in highlights else ""
                    st.markdown(f'<div class="data-node {style_class}">{val}</div>', unsafe_allow_html=True)
                    st.caption(f"Index {i}")
        else:
            viz_placeholder.warning("المصفوفة فارغة")

    render_visuals()

    if execute_btn:
        if op == "إضافة (Insert)":
            status_log.info("جاري استدعاء أمر الإضافة..." if "الدوال" in code_style else "تنفيذ سطر الإضافة...")
            time.sleep(0.5)
            st.session_state.array_list.append(input_val)
            render_visuals([len(st.session_state.array_list)-1])
            st.success("✅ تمت العملية")

        elif op == "حذف (Delete)":
            idx = int(input_val) if input_val.isdigit() else 0
            if idx < len(st.session_state.array_list):
                render_visuals([idx])
                time.sleep(0.8)
                st.session_state.array_list.pop(idx)
                render_visuals()
                st.success("✅ تم الحذف")

        elif op == "بحث (Search)":
            for i, v in enumerate(st.session_state.array_list):
                render_visuals([i])
                time.sleep(0.5)
                if v == input_val:
                    st.balloons()
                    st.success("🎯 تم العثور على القيمة")
                    break

        elif op == "ترتيب (Sort)":
            arr = st.session_state.array_list
            n = len(arr)
            for i in range(n):
                for j in range(0, n-i-1):
                    render_visuals([j, j+1])
                    time.sleep(0.4)
                    if int(arr[j]) > int(arr[j+1]):
                        arr[j], arr[j+1] = arr[j+1], arr[j]
                        render_visuals([j, j+1])
                        time.sleep(0.4)
            st.session_state.array_list = arr
            render_visuals()
            st.success("✅ الترتيب مكتمل")

    st.markdown('</div>', unsafe_allow_html=True)



st.divider()
st.info("💡 لاحظ الفرق: الأسلوب التقليدي يكتب الكود مباشرة، بينما أسلوب الدوال يقوم بتعريف وظيفة مستقلة ثم استدعائها باسمها.")