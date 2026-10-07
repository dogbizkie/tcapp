import streamlit as st
import pandas as pd
import math
import io

# --- 1. DATABASES & PRICING ---

ASUWARIS_PRICES = {
    "Solid": {"6x8": 646, "6x12": 852, "6x14": 1003},
    "Woodgrain": {"6x8": 656, "6x12": 867, "6x14": 1019},
    "Solid TX": {"6x8": 686, "6x12": 892, "6x14": 1053},
    "Woodgrain TX": {"6x8": 696, "6x12": 907, "6x14": 1069}
}
FORMICA_PRICES = {
    "Solid": {"6x9": 1043, "6x12": 1391, "6x14": 1622},
    "Woodgrain": {"6x9": 1070, "6x12": 1427, "6x14": 1665},
    "Solid TX": {"6x9": 1093, "6x12": 1441, "6x14": 1672},
    "Woodgrain TX": {"6x9": 1120, "6x12": 1477, "6x14": 1715}
}

BOARD_DIMS = {
    "6x8": (1830, 2440), "6x9": (1830, 2745), 
    "6x12": (1830, 3660), "6x14": (1830, 4270)
}

ACCESSORIES_DB = {
    "Legs": {
        "None": 0.00,
        "A116 - Nylon Leg - New (10, 13 & 18mm)": 11.00,
        "A101 - Nylon Leg - Old (10, 13 & 18mm)": 9.50,
        "A125 - Stainless Steel Leg (10, 13 & 18mm) (Asuwaris)": 25.00
    },
    "Hooks": {
        "None": 0.00,
        "A128 - Stainless Steel Coat Hook (Old Stock)": 8.80,
        "A102 - Nylon Coat Hook - Old": 5.00,
        "A117 - Nylon Coat Hook - New": 4.10,
        "A111 - Stainless Steel Coat Hook c/w Door Stop (China)": 6.90,
        "A402 - Stainless Steel Coat Hook with capping": 7.50
    },
    "Hinges": {
        "None": 0.00,
        "A110 - Stainless Steel Hinge - T31 (10mm) : L/R (China)": 19.00,
        "A121 - Nylon Hinges - New (L/R)": 11.20,
        "A110X - Stainless Steel Hinge - T31 (12mm & 13mm) : L/R (China)": 24.20,
        "A110XX - Stainless Steel Hinge - T51 (18mm) : L/R (China)": 22.10,
        "A118 - Stainless Steel Conceal Hinge (Local)": 10.00,
        "A113 - Stainless Steel Doric Hinge (China)": 9.50,
        "A110M - Stainless Steel Hinge - T21 (10mm) : L/R (Maghin)": 30.00,
        "A110MX - Stainless Steel Hinge - T31 (12/13mm) : L/R (Maghin)": 40.00,
        "A110MXX - Stainless Steel Hinge - T51 (18mm) : L/R (Maghin)": 60.00
    },
    "Door Knobs": {
        "None": 0.00,
        "A104 - Nylon Doorknob - Old (set)": 8.00,
        "A515 - Stainless Steel Door Knob(Small) China": 13.70
    },
    "Locksets": {
        "None": 0.00,
        "A326M - Stainless Steel Lockset (Maghin)": 90.00,
        "A106 - Nylon Lockset - Old": 8.50,
        "A119 - Bezault Lockset - New": 10.60,
        "A107 - Stainless Steel Lockset (136) China": 29.50,
        "A109 - Stainless Steel Lockset (TL 600) - Door Frame (Old)": 19.50,
        "A109A - Stainless Steel Lockset (TL 800)": 22.00,
        "A326 - Stainless Steel Lockset (China)": 51.00,
        "S116M - Sliding Door Lockset - Maghin": 60.00,
        "A107M - Stainless Steel Lockset (136) Maghin": 45.00,
        "A129M - Stainless Steel Lockset (236) Maghin": 90.00,
        "A216M - Stainless Steel Lockset (L/R) Maghin": 100.00
    },
    "Shoeboxes": {
        "None": 0.00,
        "SS400 - Size 100mm x 400mm (L)": 31.00,
        "ASB6100B - Aluminium Shoe Box + Angle - Black : 6.1m": 94.00,
        "ASB6100NA - Aluminium Shoe Box + Angle - N/A : 6.1m": 85.50,
        "ASBCAPPING - Aluminium Shoe Capping (Black & Grey)": 1.75,
        "SS100 - Size 100mm x 100mm (L)": 13.50,
        "SS200 - Size 100mm x 200mm (L)": 21.00,
        "SS300 - Size 100mm x 300mm (L)": 26.00,
        "SS500 - Size 100mm x 500mm (L)": 37.00,
        "SS600 - Size 100mm x 600mm (L)": 50.00,
        "SS700 - Size 100mm x 700mm (L)": 66.00,
        "SS800 - Size 100mm x 800mm (L)": 67.00,
        "SS900 - Size 100mm x 900mm (L)": 70.00,
        "SS1000 - Size 100mm x 1000mm (L)": 75.00,
        "SS1100 - Size 100mm x 1100mm (L)": 76.00,
        "SS1200 - Size 100mm x 1200mm (L)": 77.00,
        "SS1300 - Size 100mm x 1300mm (L)": 141.00,
        "SS1400 - Size 100mm x 1400mm (L)": 143.00,
        "SS1500 - Size 100mm x 1500mm (L)": 146.00,
        "SS1600 - Size 100mm x 1600mm (L)": 148.00,
        "SS1700 - Size 100mm x 1700mm (L)": 150.00,
        "SS1800 - Size 100mm x 1800mm (L)": 152.00,
        "SS1900 - Size 100mm x 1900mm (L)": 183.00,
        "SS2000 - Size 100mm x 2000mm (L)": 186.00
    },
    "L-Brackets": {
        "None": 0.00,
        "A122 - Nylon L-Bracket - New": 1.50,
        'A127 - Stainless Steel L-Bracket (2" x 2") China': 3.00,
        'A127x - Stainless Steel L-Bracket (2" x 3") Asuwaris': 3.00
    },
    "U-Channels": {
        "None": 0.00,
        "106100B - Aluminium U-Channel - Black : 6.1m (10mm)": 36.50,
        "106100NA - Aluminium U-Channel - N/A : 6.1m (10mm)": 32.50,
        "126100B - Aluminium U-Channel - Black : 6.1m (12 & 13mm)": 37.80,
        "126100NA - Aluminium U-Channel - N/A : 6.1m (12 & 13mm)": 33.50,
        "186100B - Aluminium U-Channel - Black : 6.1m (18mm)": 39.00,
        "186100NA - Aluminium U-Channel - N/A : 6.1m (18mm)": 33.50
    },
    "Headrails": {
        "None": 0.00,
        "HRT6100B - Aluminium Triangle Headrail - Black : 6.1m": 75.00,
        "HRO6100B - Aluminium Oval Headrail - Black : 6.1m": 99.00,
        "HRO6100NA - Aluminium Oval Headrail - N/A : 6.1m": 94.00,
        "HRSQ6100B - Aluminium Square Headrail - Black : 6.1m": 116.00,
        "HRSQ6100NA - Aluminium Square Headrail - N/A : 6.1m": 115.00,
        "HRT6100NA - Aluminium Triangle Headrail - N/A : 6.1m": 76.00
    },
    "Door Jambs": {
        "None": 0.00,
        "18DJNA6100 - Aluminium Door Jamb - N/A : 6.1m (18mm)": 27.00,
        "10DJB6100 - Aluminium Door Jamb - Black : 6.1m (10mm)": 23.50,
        "10DJNA6100 - Aluminium Door Jamb - N/A : 6.1m (10mm)": 21.00,
        "12DJB6100 - Aluminium Door Jamb - Black : 6.1m (12 & 13mm)": 26.00,
        "12DJNA6100 - Aluminium Door Jamb - N/A : 6.1m (12 & 13mm)": 22.00,
        "18DJB6100 - Aluminium Door Jamb - Black : 6.1m (18mm)": 33.00
    },
    "Door Frames": {
        "None": 0.00,
        "DFO4200NA - Aluminium Door Frame (Old) + Angle - N/A : 4.2m": 125.00,
        "DFO4200B - Aluminium Door Frame (Old) + Angle - Black : 4.2m": 137.00,
        "DFN4200B - Aluminium Door Frame (New) + Angle - Black : 4.2m": 100.00,
        "DFN4200NA - Aluminium Door Frame (New) + Angle - N/A : 4.2m": 98.00,
        "DFO4200GHB - Aluminium Door Frame (Old) c/w Gear Hinge - Black : 4.2m": 154.00,
        "DFO4200GHNA - Aluminium Door Frame (Old) c/w Gear Hinge - N/A : 4.2m": 141.00
    },
    "Aluminium Profiles": {
        "None": 0.00,
        'LANGLE1X26100NA - Aluminium L-Angle (1" x 2") - N/A : 6.1m': 46.50,
        "CRNR6100B - Aluminium Corner - Black : 6.1m": 62.00,
        "CRNR6100NA - Aluminium Corner - N/A : 6.1m": 56.00,
        "SQPOLE6100B - Aluminium Square Pole - Black : 6.1m": 98.00,
        "SQPOLE6100NA - Aluminium Square Pole - N/A : 6.1m": 94.50,
        "AGH4000B - Aluminium Gear Hinge - Black : 4.0m": 77.00,
        "AGH4000NA - Aluminium Gear Hinge - N/A : 4.0m": 74.00,
        'LANGLE1X26100B - Aluminium L-Angle (1" x 2") - Black : 6.1m': 53.00,
        'LANGLE2X26100B - Aluminium L-Angle (2" x 2") - Black : 6.1m': 66.00,
        'LANGLE2X26100NA - Aluminium L-Angle (2" x 2") - N/A : 6.1m': 62.50,
        'LANGLE2X26100B3 - Aluminium L-Angle (2" x 2" x 3mm) Black': 114.00,
        'LANGLE2X26100NA3 - Aluminium L-Angle (2" x 2" x 3mm) NA': 116.00,
        "FCHANN6100B - Aluminium F-Channel - 6.1m (Black)": 75.00,
        "FCHANN6100NA - Aluminium F-Channel - 6.1m (NA)": 69.50,
        "FB6100NA - Aluminium Flat Bar - 6.1m (NA)": 19.00,
        "FB6100B - Aluminium Flat Bar - 6.1m (Black)": 21.00,
        "JBAR6100 - Aluminium J Bar - MF : 6.1m": 53.50,
        "SBAR6100 - Aluminium S Bar - MF : 6.1m": 58.00,
        "AROUNDTUBE - Aluminium Round Tube - Black : 6.1m": 64.50
    },
    "Others": {
        "None": 0.00,
        "A325M - Stainless Steel Door Handle (Big) Maghin": 60.00,
        "A103M - Nylon Toilet Roll Holder - New (Maghin)": 30.00
    }
}

TRANSPORT_DB = {
    "Kuala Lumpur": {"1 Tonne": 120, "3 Tonne": 195},
    "Shah Alam": {"1 Tonne": 135, "3 Tonne": 210},
    "Klang": {"1 Tonne": 155, "3 Tonne": 235},
    "Seremban": {"1 Tonne": 290, "3 Tonne": 360},
    "Melaka": {"1 Tonne": 510, "3 Tonne": 640},
    "Johor Bahru": {"1 Tonne": 780, "3 Tonne": 980},
    "Penang": {"1 Tonne": 790, "3 Tonne": 980}
}

LABOR_DB = {}
labor_groups = [
    (["KL & PJ"], 100, [120, 125, 125, 165], [137, 144, 144, 186], [0, 200, 200, 245], [96, 101, 101, 135], [83, 90, 90, 125]),
    (["Shah Alam", "Klang"], 100, [124, 130, 130, 170], [148, 154, 154, 200], [0, 206, 206, 250], [101, 107, 107, 140], [90, 96, 96, 130])
]
for locs, meas, scan, orient, monitor, tech3, tech1 in labor_groups:
    for loc in locs:
        LABOR_DB[loc] = {
            "Scan": {"10mm": [meas, scan[0]], "12mm": [meas, scan[1]], "13mm": [meas, scan[2]], "18mm": [meas, scan[3]]},
            "Orient": {"10mm": [meas, orient[0]], "12mm": [meas, orient[1]], "13mm": [meas, orient[2]], "18mm": [meas, orient[3]]},
            "Monitor": {"10mm": [meas, monitor[0]], "12mm": [meas, monitor[1]], "13mm": [meas, monitor[2]], "18mm": [meas, monitor[3]]},
            "Tech 3": {"10mm": [meas, tech3[0]], "12mm": [meas, tech3[1]], "13mm": [meas, tech3[2]], "18mm": [meas, tech3[3]]},
            "Tech 1": {"10mm": [meas, tech1[0]], "12mm": [meas, tech1[1]], "13mm": [meas, tech1[2]], "18mm": [meas, tech1[3]]}
        }


# --- INITIALIZE STATE FOR CUMULATIVE LISTS ---
if 'mat_df' not in st.session_state:
    st.session_state.mat_df = pd.DataFrame(columns=["Item", "Unit Cost (RM)", "Qty"])
if 'log_df' not in st.session_state:
    st.session_state.log_df = pd.DataFrame(columns=["Item", "Unit Cost (RM)", "Qty"])
if 'calc_done' not in st.session_state:
    st.session_state.calc_done = False
if 'doors_count' not in st.session_state:
    st.session_state.doors_count = 0
if 'cutting_html' not in st.session_state:
    st.session_state.cutting_html = ""
if 'extra_boards_warning' not in st.session_state:
    st.session_state.extra_boards_warning = 0

# --- 2. STREAMLIT UI SETUP ---
st.set_page_config(page_title="Cubicle Costing App", layout="wide")
st.title("Full-Fledged Cubicle Costing App")

st.sidebar.header("1. Project Settings")
sys_series = st.sidebar.selectbox("System Series", ["Scan", "Orient", "Monitor", "Tech 1", "Tech 3"])
brand = st.sidebar.selectbox("Board Brand", ["ASUWARIS", "Formica"])
finish_base = st.sidebar.selectbox("Finish Type", ["Solid", "Woodgrain"])
texture_type = st.sidebar.radio("Surface Texture", ["Non-Texture (Matte/Gloss)", "Texture (TX)"])
finish = f"{finish_base} TX" if "TX" in texture_type else finish_base

thickness = st.sidebar.selectbox("Thickness", ["10mm", "12mm", "13mm", "18mm"])
opt_mode = st.sidebar.radio("Board Stock Optimization", ["Ex-Stock (6x14 Only)", "All Stocks (Cost-Efficient)"])

st.sidebar.header("2. Engine Settings")
conn_pref = st.sidebar.radio("Partition Connector Preference", ["L-Bracket", "U-Channel"])

st.sidebar.header("3. Logistics & Labor")
area = st.sidebar.selectbox("Project Area (Labor)", list(LABOR_DB.keys()))
transport_loc = st.sidebar.selectbox("Transport Destination", list(TRANSPORT_DB.keys()))
lorry_type = st.sidebar.radio("Lorry Size", ["1 Tonne", "3 Tonne"])

# --- 3. DIMENSIONS ---
st.markdown("### Panel Dimensions & Quantities (mm)")
def get_df(w, h):
    return pd.DataFrame({"Width": [w], "Height": [h], "Qty": [0]})

col1, col2, col3 = st.columns(3)
with col1:
    st.write("**Doors**")
    df_doors = st.data_editor(get_df(600, 1800), num_rows="dynamic", key="doors", hide_index=True)
    st.write("**Int Pilasters**")
    df_int_pil = st.data_editor(get_df(300, 1800), num_rows="dynamic", key="int_pil", hide_index=True)

with col2:
    st.write("**End Pilasters**")
    df_end_pil = st.data_editor(get_df(150, 1800), num_rows="dynamic", key="end_pil", hide_index=True)
    st.write("**Dividing Panels**")
    df_div = st.data_editor(get_df(1500, 1800), num_rows="dynamic", key="div", hide_index=True)

with col3:
    st.write("**End Dividing Panels**")
    df_end_div = st.data_editor(get_df(1500, 1800), num_rows="dynamic", key="end_div", hide_index=True)
    st.write("**Urinal Panels**")
    df_uri = st.data_editor(get_df(450, 900), num_rows="dynamic", key="uri", hide_index=True)

def get_clean_rows(df, label):
    rows = []
    for _, row in df.iterrows():
        try:
            qty = int(row.get('Qty', 0))
            w = float(row.get('Width', 0))
            h = float(row.get('Height', 0))
            if qty > 0: rows.append({"label": label, "w": w, "h": h, "qty": qty})
        except: pass
    return rows

doors = get_clean_rows(df_doors, "Door")
int_pils = get_clean_rows(df_int_pil, "Int Pil")
end_pils = get_clean_rows(df_end_pil, "End Pil")
divs = get_clean_rows(df_div, "Div Pan")
end_divs = get_clean_rows(df_end_div, "End Div")
uris = get_clean_rows(df_uri, "Urinal")

total_doors = sum(d['qty'] for d in doors)
total_int_pil = sum(p['qty'] for p in int_pils)
total_end_pil = sum(p['qty'] for p in end_pils)
total_uri = sum(u['qty'] for u in uris)

# --- 4. CALCULATE RECOMMENDATIONS ---
rec = {k: 0 for k in ACCESSORIES_DB.keys()}
rec["Legs"] = (total_int_pil * 2) + (total_end_pil * 1) if sys_series == "Scan" else 0
rec["Hooks"] = total_doors
rec["Door Knobs"] = total_doors
rec["Locksets"] = total_doors
rec["Hinges"] = sum(d['qty'] * (4 if d['h'] > 2100 else 3) for d in doors)

lb_count = sum(p['qty'] * (8 if p['h'] > 2100 else 6) for p in divs + end_divs + int_pils) + \
           sum(p['qty'] * (4 if p['h'] > 2100 else 3) for p in end_pils)
uc_mm = sum(p['qty'] * p['h'] for p in divs + end_divs + int_pils + end_pils)

if conn_pref == "L-Bracket":
    rec["L-Brackets"] = lb_count + (total_uri * 6)
    rec["U-Channels"] = 0
else:
    rec["L-Brackets"] = (total_uri * 6)
    rec["U-Channels"] = math.ceil(uc_mm / 6100) if uc_mm > 0 else 0

hr_width = sum(d['qty'] * d['w'] for d in doors) + sum(p['qty'] * p['w'] for p in int_pils + end_pils)
rec["Headrails"] = math.ceil((hr_width * 1.10) / 6100) if (sys_series in ["Scan", "Orient"] and hr_width > 0) else 0

df_len = sum(d['qty'] * ((d['h'] * 2) + d['w']) for d in doors)
rec["Door Frames"] = math.ceil(df_len / 4200) if (sys_series == "Tech 1" and df_len > 0) else 0


# --- 5. HARDWARE CONFIGURATOR ---
st.markdown("---")
st.markdown("### Hardware Configurator")
st.markdown("<span style='font-size: 0.9em; color: gray;'>Engine recommendations are shown in <span style='color: red;'>red</span> based on your dimensions. Add quantities below to send them to the final breakdown.</span>", unsafe_allow_html=True)

h1, h2, h3, h4, h5 = st.columns([1.5, 4, 1, 1, 1.5])
h1.write("**Type**")
h2.write("**Model & Description**")
h3.write("**Cost**")
h4.write("**Quantity**")
h5.write("**Total Cost**")
st.markdown("<hr style='margin: 0px 0px 10px 0px;'>", unsafe_allow_html=True)

hw_selections = {}

def hw_row(type_label, db_category):
    c1, c2, c3, c4, c5 = st.columns([1.5, 4, 1, 1, 1.5])
    rec_val = rec.get(db_category, 0)
    
    with c1:
        st.markdown(f"**{type_label}**")
        if rec_val > 0:
            st.markdown(f"<span style='color:red; font-size:12px; font-weight:bold;'>Rec: {rec_val}</span>", unsafe_allow_html=True)
    with c2:
        sel = st.selectbox("Item", list(ACCESSORIES_DB[db_category].keys()), key=f"sel_{type_label}", label_visibility="collapsed")
    with c3:
        cost = ACCESSORIES_DB[db_category][sel]
        st.markdown(f"<div style='margin-top:8px;'>{cost:.2f}</div>", unsafe_allow_html=True)
    with c4:
        qty = st.number_input("Qty", min_value=0, value=rec_val, key=f"qty_{type_label}", label_visibility="collapsed")
    with c5:
        st.markdown(f"<div style='margin-top:8px;'>{cost * qty:.2f}</div>", unsafe_allow_html=True)
        
    if qty > 0 and sel != "None":
        hw_selections[sel] = {"Cost": cost, "Qty": qty}

hw_row("Adjustable Leg", "Legs")
hw_row("Coat Hook", "Hooks")
hw_row("Hinges", "Hinges")
hw_row("Door Knob", "Door Knobs")
hw_row("Lockset", "Locksets")
hw_row("Skirting / Shoebox", "Shoeboxes")
hw_row("L Brackets", "L-Brackets")
hw_row("U Channel", "U-Channels")
hw_row("Headrail", "Headrails")
hw_row("Door Jamb", "Door Jambs")
hw_row("Door Frame", "Door Frames")
hw_row("Aluminium Acc", "Aluminium Profiles")
hw_row("Others", "Others")

# --- 6. NESTING ENGINE ---
def generate_cutting_list(panels_list, allocated_boards, is_woodgrain):
    items = []
    kerf = 5
    for p in panels_list:
        for _ in range(p['qty']):
            w, h = p['w'] + kerf, p['h'] + kerf
            if not is_woodgrain:
                if w > h: w, h = h, w
            items.append({'label': p['label'], 'w': w, 'h': h, 'ow': p['w'], 'oh': p['h']})
            
    items.sort(key=lambda x: x['h'], reverse=True)
    allocated_boards.sort(key=lambda x: x['h'], reverse=True)
    
    boards = [{'w': b['w'], 'h': b['h'], 'name': b['name'], 'shelves': [], 'used_h': 0} for b in allocated_boards]
    unpacked_items = []
    
    for item in items:
        placed = False
        for board in boards:
            for shelf in board['shelves']:
                if shelf['used_w'] + item['w'] <= board['w'] and item['h'] <= shelf['h']:
                    item['x'], item['y'] = shelf['used_w'], shelf['y']
                    shelf['items'].append(item)
                    shelf['used_w'] += item['w']
                    placed = True
                    break
            if placed: break
            
            if board['used_h'] + item['h'] <= board['h']:
                new_shelf = {'y': board['used_h'], 'h': item['h'], 'used_w': item['w'], 'items': [item]}
                item['x'], item['y'] = 0, board['used_h']
                board['shelves'].append(new_shelf)
                board['used_h'] += item['h']
                placed = True
                break
        if not placed:
            unpacked_items.append(item)
            
    extra_count = 0
    while unpacked_items:
        new_board = {'w': 1830, 'h': 4270, 'name': '6x14 (Extra Overflow)', 'shelves': [], 'used_h': 0}
        boards.append(new_board)
        extra_count += 1
        
        items_to_pack = unpacked_items[:]
        unpacked_items = []
        for item in items_to_pack:
            placed = False
            for board in boards[-extra_count:]: 
                for shelf in board['shelves']:
                    if shelf['used_w'] + item['w'] <= board['w'] and item['h'] <= shelf['h']:
                        item['x'], item['y'] = shelf['used_w'], shelf['y']
                        shelf['items'].append(item)
                        shelf['used_w'] += item['w']
                        placed = True
                        break
                if placed: break
                if board['used_h'] + item['h'] <= board['h']:
                    new_shelf = {'y': board['used_h'], 'h': item['h'], 'used_w': item['w'], 'items': [item]}
                    item['x'], item['y'] = 0, board['used_h']
                    board['shelves'].append(new_shelf)
                    board['used_h'] += item['h']
                    placed = True
                    break
            if not placed: unpacked_items.append(item)
            
    return boards, extra_count

def render_cutting_html(boards, is_woodgrain):
    html = "<div style='display:flex; flex-wrap:wrap; gap: 20px;'>"
    scale = 0.08 
    bg_css = "background: repeating-linear-gradient(to bottom, #deb887, #deb887 2px, #d2b48c 2px, #d2b48c 4px);" if is_woodgrain else "background: #add8e6;"
    
    for i, board in enumerate(boards):
        html += f"<div style='border: 2px solid #333; width: {board['w'] * scale}px; height: {board['h'] * scale}px; position: relative; background: #fff; margin-bottom: 25px;'>"
        for shelf in board['shelves']:
            for item in shelf['items']:
                html += f"<div style='position: absolute; left: {item['x'] * scale}px; top: {item['y'] * scale}px; width: {item['w'] * scale}px; height: {item['h'] * scale}px; border: 1px solid #000; {bg_css} display:flex; align-items:center; justify-content:center; overflow: hidden;'>"
                html += f"<span style='background:rgba(255,255,255,0.7); font-size:10px; padding:2px; text-align:center;'><b>{item['label']}</b><br>{item['ow']}x{item['oh']}</span>"
                html += "</div>"
        html += f"<div style='position: absolute; bottom: -20px; width: 100%; text-align: center; font-weight: bold; font-size:14px;'>Board {i+1} ({board['name']})</div>"
        html += "</div>"
    html += "</div>"
    return html

# --- 7. BUTTONS LOGIC ---
st.markdown("---")
c_btn1, c_btn2 = st.columns(2)

with c_btn2:
    if st.button("🗑️ Clear & Reset Breakdown", use_container_width=True):
        st.session_state.mat_df = pd.DataFrame(columns=["Item", "Unit Cost (RM)", "Qty"])
        st.session_state.log_df = pd.DataFrame(columns=["Item", "Unit Cost (RM)", "Qty"])
        st.session_state.cutting_html = ""
        st.session_state.extra_boards_warning = 0
        st.session_state.calc_done = False
        st.rerun()

with c_btn1:
    if st.button("➕ Update / Add to Materials Breakdown", type="primary", use_container_width=True):
        
        current_list = st.session_state.mat_df.to_dict('records')
        
        # Board Yield Calculation
        kerf = 5
        total_area = 0
        all_panels = doors + int_pils + end_pils + uris
        if sys_series not in ["Tech 1", "Tech 3"]:
            all_panels += divs + end_divs
            
        for item in all_panels:
            total_area += item['qty'] * (item['w'] + kerf) * (item['h'] + kerf)

        price_dict = ASUWARIS_PRICES[finish] if brand == "ASUWARIS" else FORMICA_PRICES[finish]
        used_boards = {}
        allocated_boards = []
        
        if total_area > 0:
            if opt_mode == "Ex-Stock (6x14 Only)":
                b_name = "6x14"
                a_b = BOARD_DIMS[b_name][0] * BOARD_DIMS[b_name][1] * 0.85
                qty = math.ceil(total_area / a_b)
                used_boards[b_name] = qty
                for _ in range(qty): allocated_boards.append({'w': BOARD_DIMS[b_name][0], 'h': BOARD_DIMS[b_name][1], 'name': b_name})
            else:
                sizes = ["6x14", "6x12", "6x8"] if brand == "ASUWARIS" else ["6x14", "6x12", "6x9"]
                s14, s12, sSmall = sizes[0], sizes[1], sizes[2]
                a14, a12, aSmall = BOARD_DIMS[s14][0]*BOARD_DIMS[s14][1]*0.85, BOARD_DIMS[s12][0]*BOARD_DIMS[s12][1]*0.85, BOARD_DIMS[sSmall][0]*BOARD_DIMS[sSmall][1]*0.85
                p14, p12, pSmall = price_dict[s14], price_dict[s12], price_dict[sSmall]
                
                best_cost = float('inf')
                best_combo = {}
                for n_14 in range(math.ceil(total_area / a14) + 1):
                    for n_12 in range(math.ceil(total_area / a12) + 1):
                        covered = (n_14 * a14) + (n_12 * a12)
                        n_small = 0 if covered >= total_area else math.ceil((total_area - covered) / aSmall)
                        cost = (n_14 * p14) + (n_12 * p12) + (n_small * pSmall)
                        if cost < best_cost:
                            best_cost, best_combo = cost, {s14: n_14, s12: n_12, sSmall: n_small}
                used_boards = {k: v for k, v in best_combo.items() if v > 0}
                for k, v in used_boards.items():
                    for _ in range(v): allocated_boards.append({'w': BOARD_DIMS[k][0], 'h': BOARD_DIMS[k][1], 'name': k})

        # Run 2D Packer
        is_woodgrain = "Woodgrain" in finish
        packed_boards, extra_boards = generate_cutting_list(all_panels, allocated_boards, is_woodgrain)
        st.session_state.cutting_html = render_cutting_html(packed_boards, is_woodgrain)
        st.session_state.extra_boards_warning = extra_boards

        # Update List
        current_list = [row for row in current_list if not str(row.get("Item", "")).startswith("Raw Board")]
        
        for b_size, qty in used_boards.items():
            current_list.insert(0, {"Item": f"Raw Board ({brand} {finish} {b_size})", "Unit Cost (RM)": price_dict[b_size], "Qty": qty})

        for sel, data in hw_selections.items():
            found = False
            for row in current_list:
                if row.get("Item") == sel:
                    row["Qty"] = data["Qty"]
                    row["Unit Cost (RM)"] = data["Cost"]
                    found = True
                    break
            if not found:
                current_list.append({"Item": sel, "Unit Cost (RM)": data["Cost"], "Qty": data["Qty"]})

        st.session_state.mat_df = pd.DataFrame(current_list)

        # Handle Logistics
        log_list = st.session_state.log_df.to_dict('records')
        log_list = [r for r in log_list if not (str(r.get("Item","")).startswith("Measurement Fee") or 
                                                str(r.get("Item","")).startswith("Installation Labor") or 
                                                str(r.get("Item","")).startswith("Transport"))]
        try:
            rates = LABOR_DB[area][sys_series][thickness]
            log_list.append({"Item": f"Measurement Fee ({area})", "Unit Cost (RM)": rates[0], "Qty": 1})
            if total_doors > 0:
                log_list.append({"Item": f"Installation Labor ({sys_series} {thickness})", "Unit Cost (RM)": rates[1], "Qty": total_doors})
        except KeyError: pass
        try:
            log_list.append({"Item": f"Transport ({transport_loc} - {lorry_type})", "Unit Cost (RM)": TRANSPORT_DB[transport_loc][lorry_type], "Qty": 1})
        except KeyError: pass

        st.session_state.log_df = pd.DataFrame(log_list)
        st.session_state.calc_done = True
        st.session_state.doors_count = total_doors
        st.rerun()


# --- 8. FINAL QUOTATION & VISUALIZER ---
if st.session_state.calc_done:
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.subheader("Final Materials Breakdown")
        edited_mat = st.data_editor(
            st.session_state.mat_df,
            column_config={
                "Item": st.column_config.TextColumn("Item / Description"),
                "Unit Cost (RM)": st.column_config.NumberColumn("Unit Cost (RM)", format="%.2f"),
                "Qty": st.column_config.NumberColumn("Qty", min_value=0)
            },
            num_rows="dynamic", hide_index=True, use_container_width=True
        )
        
        mat_total = 0
        if not edited_mat.empty and "Qty" in edited_mat.columns and "Unit Cost (RM)" in edited_mat.columns:
            edited_mat["Total"] = pd.to_numeric(edited_mat["Qty"], errors='coerce').fillna(0) * pd.to_numeric(edited_mat["Unit Cost (RM)"], errors='coerce').fillna(0)
            mat_total = edited_mat["Total"].sum()
            
        st.metric("Total Material Cost", f"RM {mat_total:,.2f}")

    with c2:
        st.subheader("Final Logistics")
        edited_log = st.data_editor(
            st.session_state.log_df,
            column_config={
                "Item": st.column_config.TextColumn("Item / Description"),
                "Unit Cost (RM)": st.column_config.NumberColumn("Unit Cost (RM)", format="%.2f"),
                "Qty": st.column_config.NumberColumn("Qty", min_value=0)
            },
            num_rows="dynamic", hide_index=True, use_container_width=True
        )
        
        log_total = 0
        if not edited_log.empty and "Qty" in edited_log.columns and "Unit Cost (RM)" in edited_log.columns:
            edited_log["Total"] = pd.to_numeric(edited_log["Qty"], errors='coerce').fillna(0) * pd.to_numeric(edited_log["Unit Cost (RM)"], errors='coerce').fillna(0)
            log_total = edited_log["Total"].sum()
            
        st.metric("Total Logistics Cost", f"RM {log_total:,.2f}")
        
        st.markdown("---")
        st.subheader("Markups & Margins")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            wastage_pct = st.number_input("Wastage (%)", min_value=0.0, value=5.0, step=1.0)
        with col_m2:
            overhead_pct = st.number_input("Overhead (%)", min_value=0.0, value=20.0, step=1.0)
        with col_m3:
            margin_pct = st.number_input("Margin (%)", min_value=0.0, value=10.0, step=1.0)
            
        wastage_amt = mat_total * (wastage_pct / 100.0)
        overhead_amt = (mat_total + log_total + wastage_amt) * (overhead_pct / 100.0)
        total_cost = mat_total + log_total + wastage_amt + overhead_amt
        margin_amt = total_cost * (margin_pct / 100.0)
        
        st.write(f"**Wastage Cost:** RM {wastage_amt:,.2f}")
        st.write(f"**Overhead Cost:** RM {overhead_amt:,.2f}")
        st.write(f"**Profit Margin:** RM {margin_amt:,.2f}")
        
        st.markdown("---")
        st.subheader("Project Grand Total (Selling Price)")
        grand_total = total_cost + margin_amt
        st.metric("Grand Total (RM)", f"RM {grand_total:,.2f}")
        
        if st.session_state.doors_count > 0:
            st.write(f"**Estimated Price per Cubicle:** RM {grand_total / st.session_state.doors_count:,.2f}")

    st.session_state.mat_df = edited_mat
    st.session_state.log_df = edited_log

    # 2D Visualizer Render
    st.markdown("---")
    st.subheader("✂️ 2D Board Cutting Layout (Heuristic Packing)")
    
    if st.session_state.extra_boards_warning > 0:
        st.warning(f"**Heuristic Overflow Warning:** The 85% area average yield underestimated the specific physical cuts needed for your dimensions. The packer requires **{st.session_state.extra_boards_warning} extra 6x14 board(s)** to fit everything. You may want to manually update the Raw Boards quantity in the table above.")
    else:
        st.success("All pieces packed successfully within the estimated 85% area yield.")
        
    st.markdown(st.session_state.cutting_html, unsafe_allow_html=True)

    # --- 9. EXCEL EXPORT ---
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        edited_mat.to_excel(writer, sheet_name="Materials", index=False)
        edited_log.to_excel(writer, sheet_name="Logistics", index=False)
        
        summary_df = pd.DataFrame({
            "Description": [
                "Total Material Cost", 
                "Total Logistics Cost", 
                f"Wastage Cost ({wastage_pct}%)", 
                f"Overhead Cost ({overhead_pct}%)", 
                f"Profit Margin ({margin_pct}%)", 
                "Project Grand Total", 
                "Estimated Price per Cubicle"
            ],
            "Amount (RM)": [
                mat_total, 
                log_total, 
                wastage_amt, 
                overhead_amt, 
                margin_amt, 
                grand_total, 
                grand_total / st.session_state.doors_count if st.session_state.doors_count > 0 else 0
            ]
        })
        summary_df.to_excel(writer, sheet_name="Project Summary", index=False)
        
    excel_data = output.getvalue()
    
    st.markdown("---")
    st.subheader("📥 Export Quotation")
    st.download_button(
        label="Download to Excel (.xlsx)",
        data=excel_data,
        file_name="Cubicle_Quotation.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )
