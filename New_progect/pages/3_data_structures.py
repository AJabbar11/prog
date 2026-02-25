import streamlit as st
import math

# --- 1. إعدادات الصفحة والتنسيق ---
st.set_page_config(page_title="مختبر هياكل البيانات الاحترافي", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050510; color: white; }
    
    /* حاوية الرسم المتجاوبة */
    .main-canvas {
        position: relative;
        width: 100%;
        height: 600px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(0, 210, 255, 0.2);
        border-radius: 25px;
        margin-top: 20px;
        overflow: hidden;
    }

    /* العقدة المضيئة */
    .data-node {
        width: 65px; height: 65px;
        background: radial-gradient(circle, #1a1c23 0%, #050510 100%);
        border: 2px solid #00d2ff;
        border-radius: 50%;
        display: flex; justify-content: center; align-items: center;
        font-weight: bold; position: absolute;
        transform: translate(-50%, -50%);
        z-index: 10;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.4);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 12px;
    }

    /* الأسلاك الذكية */
    .connector-svg {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: 5;
    }

    /* المؤشرات البرمجية */
    .ptr-label {
        position: absolute;
        color: #ff00ff;
        font-weight: bold;
        font-size: 13px;
        text-shadow: 0 0 10px #ff00ff;
        z-index: 15;
        white-space: nowrap;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة مخازن البيانات (تصحيح المفاتيح) ---
if 'ds' not in st.session_state:
    st.session_state.ds = {
        "Binary Tree": ["Root", "L1", "R1"],
        "Stack": ["Base", "Mid", "Top"],
        "Queue": ["Front", "Mid", "Rear"],
        "Circular List": ["C1", "C2", "C3"]
    }

# --- 3. الواجهة العلوية (الخيارات في الأعلى) ---
st.title("🛡️ محاكي هياكل البيانات التفاعلي")

# استخدام أعمدة للخيارات العلوية
col_opt1, col_opt2, col_opt3 = st.columns([2, 2, 2])

with col_opt1:
    ds_choice = st.selectbox("اختر الهيكل:", ["Binary Tree", "Stack", "Queue", "Circular List"])
with col_opt2:
    new_node_val = st.text_input("قيمة العقدة الجديدة:", "Node_" + str(len(st.session_state.ds[ds_choice])))
with col_opt3:
    st.write("##") # للموازنة
    btn_add, btn_del = st.columns(2)
    if btn_add.button("➕ إضافة", use_container_width=True):
        st.session_state.ds[ds_choice].append(new_node_val)
        st.rerun()
    if btn_del.button("🗑️ حذف", use_container_width=True):
        if st.session_state.ds[ds_choice]:
            # منطق الحذف حسب الهيكل
            if ds_choice == "Queue":
                st.session_state.ds[ds_choice].pop(0) # FIFO
            else:
                st.session_state.ds[ds_choice].pop() # LIFO / Tree
            st.rerun()

# --- 4. محرك الحسابات الجيومترية والكود البرمجي ---
data = st.session_state.ds[ds_choice]
n = len(data)
coords = [] # (x%, y%)
java_logic = ""

if ds_choice == "Binary Tree":
    for i in range(n):
        if i == 0: coords.append((50, 15))
        else:
            lvl = int(math.log2(i + 1))
            parent = (i - 1) // 2
            px, py = coords[parent]
            off = 25 / (lvl + 0.5)
            x = px - off if i % 2 != 0 else px + off
            coords.append((x, py + 20))
    java_logic = f"// Binary Tree Implementation\nTreeNode root = new TreeNode('{data[0]}');\nroot.left = new TreeNode('{new_node_val}');"

elif ds_choice == "Stack":
    for i in range(n):
        coords.append((50, 15 + (i * 12)))
    java_logic = f"// Stack Implementation (LIFO)\nStack<String> stack = new Stack<>();\nstack.push('{new_node_val}');"

elif ds_choice == "Queue":
    # عرض أفقي للطابور
    for i in range(n):
        coords.append((20 + (i * (60/max(n,1))), 50))
    java_logic = f"// Queue Implementation (FIFO)\nQueue<String> queue = new LinkedList<>();\nqueue.add('{new_node_val}');"

elif ds_choice == "Circular List":
    radius = 20
    for i in range(n):
        angle = (2 * math.pi * i) / n
        coords.append((50 + radius * math.cos(angle), 50 + radius * 1.2 * math.sin(angle)))
    java_logic = f"// Circular Linked List\nNode temp = new Node('{new_node_val}');\nlast.next = temp;\ntemp.next = head;"

# --- 5. العرض البصري المترابط مع الكود ---
col_viz, col_code = st.columns([2.5, 1])

with col_viz:
    html = '<div class="main-canvas">'
    # رسم الأسلاك (SVG)
    svg = '<svg class="connector-svg" viewBox="0 0 100 100" preserveAspectRatio="none">'
    for i in range(n):
        if ds_choice == "Binary Tree" and i > 0:
            p = (i - 1) // 2
            svg += f'<line x1="{coords[p][0]}" y1="{coords[p][1]}" x2="{coords[i][0]}" y2="{coords[i][1]}" stroke="#ff00ff" stroke-width="0.3" />'
        elif ds_choice == "Circular List" and n > 1:
            nxt = (i + 1) % n
            svg += f'<line x1="{coords[i][0]}" y1="{coords[i][1]}" x2="{coords[nxt][0]}" y2="{coords[nxt][1]}" stroke="#00d2ff" stroke-width="0.2" stroke-dasharray="1" />'
        elif (ds_choice == "Stack" or ds_choice == "Queue") and i > 0:
            svg += f'<line x1="{coords[i-1][0]}" y1="{coords[i-1][1]}" x2="{coords[i][0]}" y2="{coords[i][1]}" stroke="rgba(255,255,255,0.1)" stroke-width="0.1" />'
    svg += '</svg>'
    html += svg

    # رسم العقد والمؤشرات
    for i, (x, y) in enumerate(coords):
        is_root_or_main = (i == 0)
        node_color = "#ff00ff" if is_root_or_main else "#00d2ff"
        html += f'<div class="data-node" style="left:{x}%; top:{y}%; border-color:{node_color};">{data[i]}</div>'
        
        # إضافة المؤشرات البرمجية
        ptr = ""
        if ds_choice == "Stack" and i == n-1: ptr = "TOP"
        elif ds_choice == "Queue":
            if i == 0: ptr = "FRONT"
            if i == n-1: ptr = "REAR"
        elif ds_choice == "Binary Tree" and i == 0: ptr = "ROOT"
        
        if ptr:
            html += f'<div class="ptr-label" style="left:{x}%; top:{y}%; transform:translate(40px, -10px);">⬅️ {ptr}</div>'
    
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

with col_code:
    st.subheader("💻 الفكر البرمجي (Java)")
    st.code(java_logic, language="java")
    st.write("---")
    st.markdown(f"**الهيكل الحالي:** {ds_choice}")
    st.markdown(f"**عدد العقد:** {n}")
    

st.markdown("<br><br>", unsafe_allow_html=True)
