import streamlit as st
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime

st.set_page_config(page_title="Critical Parts Logger", page_icon="⚡", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 780px; padding-top: 2rem; }
div[data-testid="stButton"] button[kind="primary"] {
    background: #185fa5 !important; color: white !important;
    border: none !important; border-radius: 7px !important; font-weight: 600 !important;
}
div[data-testid="stDownloadButton"] button {
    background: #185fa5 !important; color: white !important;
    border: none !important; border-radius: 7px !important;
    font-weight: 600 !important; width: 100%;
}
.row-card {
    background: #f8fafd; border: 1px solid #e2ecf6;
    border-radius: 8px; padding: 0.6rem 1rem;
    margin-bottom: 0.4rem; font-size: 0.88rem; color: #2a4a68;
    display: flex; justify-content: space-between; align-items: center;
}
.row-card .left  { flex: 1; }
.row-card .right { color: #8fa5bc; font-size: 0.78rem; white-space: nowrap; margin-left: 1rem; }
</style>
""", unsafe_allow_html=True)

COMP_TYPES = [
    "VFD / Drive", "Motor", "PLC", "HMI",
    "Encoder / Resolver", "Load Cell", "Sensor",
    "Circuit Breaker / MCCB", "Relay / Contactor",
    "Transformer"
]

# ── Session State ────────────────────────────────────────────────────────────
if "parts" not in st.session_state:
    st.session_state.parts = []

if "current_machine" not in st.session_state:
    st.session_state.current_machine = None

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("## ⚡ Critical Parts Logger")
st.markdown("<div style='color:#8fa5bc;font-size:0.85rem;margin-top:-0.5rem;margin-bottom:1.5rem;'>Sapphire Fibres Limited</div>", unsafe_allow_html=True)

# ── Machine Setup ────────────────────────────────────────────────────────────
if st.session_state.current_machine is None:
    st.markdown("### ➕ Start New Machine")

    c1, c2 = st.columns(2)
    dept_input = c1.text_input("Department *", placeholder="e.g. Weaving")
    mach_input = c2.text_input("Machine *", placeholder="e.g. Loom-12")

    if st.button("Start Machine", use_container_width=True, type="primary"):
        if not dept_input.strip() or not mach_input.strip():
            st.error("Department and Machine are required.")
        else:
            st.session_state.current_machine = {
                "department": dept_input.strip(),
                "machine": mach_input.strip()
            }
            st.success(f"Started {mach_input.strip()}")

# ── Component Entry ──────────────────────────────────────────────────────────
if st.session_state.current_machine is not None:
    st.markdown(f"""
    <div style='padding:10px;background:#f4f8ff;border-radius:8px;margin-bottom:10px;'>
    <strong>Current:</strong> {st.session_state.current_machine['department']} → {st.session_state.current_machine['machine']}
    </div>
    """, unsafe_allow_html=True)

    with st.form("add_component", clear_on_submit=True):

        c3, c4 = st.columns(2)

        comp_type = c3.selectbox(
            "Component Type *",
            COMP_TYPES + ["Other (Type Manually)"]
        )

        custom_type = ""
        if comp_type == "Other (Type Manually)":
            custom_type = c3.text_input("Enter Component Type", placeholder="e.g. Servo Drive")

        final_type = custom_type.strip() if comp_type == "Other (Type Manually)" else comp_type

        name = c4.text_input("Name / Brand", placeholder="e.g. Siemens")

        c5, c6, c7 = st.columns(3)
        model = c5.text_input("Model No.", placeholder="e.g. G120")
        specs = c6.text_input("Specs", placeholder="e.g. 7.5 kW, 400 V")
        tag   = c7.text_input("Tag", placeholder="e.g. VFD-01")

        submitted = st.form_submit_button("+ Add Component", use_container_width=True)

    if submitted:
        if comp_type == "Other (Type Manually)" and not final_type:
            st.error("Please enter a custom component type.")
        else:
            st.session_state.parts.append({
                "department": st.session_state.current_machine["department"],
                "machine":    st.session_state.current_machine["machine"],
                "type":       final_type,
                "name":       name.strip(),
                "model":      model.strip(),
                "specs":      specs.strip(),
                "tag":        tag.strip(),
            })
            st.success(f"✓ {final_type} added")

    if st.button("✅ Finish Machine", use_container_width=True):
        st.session_state.current_machine = None
        st.success("Machine saved. Start another.")

# ── Parts List ───────────────────────────────────────────────────────────────
parts = st.session_state.parts

if parts:
    st.divider()

    col_h, col_clr = st.columns([4, 1])
    col_h.markdown(f"**{len(parts)} component{'s' if len(parts) != 1 else ''} logged**")
    if col_clr.button("🗑 Clear All"):
        st.session_state.parts = []
        st.rerun()

    grouped = {}
    for p in parts:
        grouped.setdefault(p["department"], {}).setdefault(p["machine"], []).append(p)

    for dept, machines in sorted(grouped.items()):
        st.markdown(f"<div style='font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#8fa5bc;border-bottom:1px solid #e4ecf3;padding-bottom:5px;margin:1rem 0 0.6rem;'>📁 {dept}</div>", unsafe_allow_html=True)
        for mach, comps in sorted(machines.items()):
            st.markdown(f"<div style='font-size:0.82rem;font-weight:600;color:#2a4a68;margin-bottom:0.4rem;'>🔧 {mach}</div>", unsafe_allow_html=True)
            for i, p in enumerate(comps):
                detail = " · ".join(filter(None, [p["name"], p["model"], p["specs"]]))
                tag_txt = f"Tag: {p['tag']}" if p["tag"] else ""
                c_card, c_del = st.columns([12, 1])
                with c_card:
                    st.markdown(f"""
                    <div class="row-card">
                        <div class="left"><strong>{p['type']}</strong>{"  —  " + detail if detail else ""}</div>
                        <div class="right">{tag_txt}</div>
                    </div>""", unsafe_allow_html=True)
                with c_del:
                    if st.button("✕", key=f"del_{dept}_{mach}_{i}"):
                        st.session_state.parts.remove(p)
                        st.rerun()

    # ── Export ───────────────────────────────────────────────────────────────
    st.divider()

    def build_excel(data):
        wb = Workbook()
        ws = wb.active
        ws.title = "Critical Parts List"

        thin   = Side(style="thin", color="D0DCEA")
        border = Border(left=thin, right=thin, top=thin, bottom=thin)

        headers    = ["Department", "Machine", "Component Type", "Name / Brand", "Model No.", "Specs", "Tag"]
        col_widths = [20, 22, 24, 20, 20, 36, 14]

        ws.append(headers)
        for ci in range(1, len(headers) + 1):
            c = ws.cell(row=1, column=ci)
            c.font      = Font(name="Arial", bold=True, color="FFFFFF", size=10)
            c.fill      = PatternFill("solid", fgColor="185FA5")
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.border    = border
        ws.row_dimensions[1].height = 24

        sorted_data = sorted(data, key=lambda p: (p["department"], p["machine"], p["type"]))
        fill_even = PatternFill("solid", fgColor="F4F8FF")
        fill_odd  = PatternFill("solid", fgColor="FFFFFF")

        for ri, p in enumerate(sorted_data, 2):
            ws.append([p["department"], p["machine"], p["type"],
                       p["name"], p["model"], p["specs"], p["tag"]])
            fill = fill_even if ri % 2 == 0 else fill_odd
            for ci in range(1, len(headers) + 1):
                c = ws.cell(row=ri, column=ci)
                c.font      = Font(name="Arial", size=10)
                c.fill      = fill
                c.alignment = Alignment(vertical="top", wrap_text=True)
                c.border    = border

        for i, w in enumerate(col_widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w

        ws.freeze_panes = "A2"
        ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"

        buf = BytesIO()
        wb.save(buf)
        buf.seek(0)
        return buf.getvalue()

    fname = f"Critical_Parts_{datetime.now().strftime('%Y%m%d')}.xlsx"
    st.download_button(
        label="⬇  Download Excel",
        data=build_excel(parts),
        file_name=fname,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
