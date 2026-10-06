import streamlit as st
import pandas as pd
import math

# --- 1. DATABASES & PRICING ---

ASUWARIS_PRICES = {
    "Solid": {"6x8": 646, "6x12": 852, "6x14": 1003},
    "Woodgrain": {"6x8": 656, "6x12": 867, "6x14": 1019}
}
FORMICA_PRICES = {
    "Solid": {"6x9": 1043, "6x12": 1391, "6x14": 1622},
    "Woodgrain": {"6x9": 1070, "6x12": 1427, "6x14": 1665}
}

BOARD_DIMS = {
    "6x8": (1830, 2440), "6x9": (1830, 2745), 
    "6x12": (1830, 3660), "6x14": (1830, 4270)
}

# Categorized Accessory Database 
ACCESSORIES_DB = {
    "Legs": {
        "None": 0.00,
        "A101 - Nylon Leg - Old (10, 13 & 18mm)": 9.50,
        "A116 - Nylon Leg - New (10, 13 & 18mm)": 11.00,
        "A125 - Stainless Steel Leg (10, 13 & 18mm) (Asuwaris)": 25.00
    },
    "Hooks": {
        "None": 0.00,
        "A102 - Nylon Coat Hook - Old": 5.00,
        "A117 - Nylon Coat Hook - New": 4.10,
        "A111 - Stainless Steel Coat Hook c/w Door Stop (China)": 6.90,
        "A128 - Stainless Steel Coat Hook (Old Stock)": 8.80,
        "A402 - Stainless Steel Coat Hook with capping": 7.50
    },
    "Door Knobs": {
        "None": 0.00,
        "A104 - Nylon Doorknob - Old (set)": 8.00,
        "A515 - Stainless Steel Door Knob(Small) China": 13.70
    },
    "Locksets": {
        "None": 0.00,
        "A106 - Nylon Lockset - Old": 8.50,
        "A119 - Bezault Lockset - New": 10.60,
        "A107 - Stainless Steel Lockset (136) China": 29.50,
        "A109 - Stainless Steel Lockset (TL 600) - Door Frame (Old)": 19.50,
        "A109A - Stainless Steel Lockset (TL 800)": 22.00,
        "A326 - Stainless Steel Lockset (China)": 51.00,
        "S116M - Sliding Door Lockset - Maghin": 60.00,
        "A107M - Stainless Steel Lockset (136) Maghin": 45.00,
        "A129M - Stainless Steel Lockset (236) Maghin": 90.00,
        "A216M - Stainless Steel Lockset (L/R) Maghin": 100.00,
        "A326M - Stainless Steel Lockset (Maghin)": 90.00
    },
    "Hinges": {
        "None": 0.00,
        "A121 - Nylon Hinges - New (L/R)": 11.20,
        "A110 - Stainless Steel Hinge - T31 (10mm) : L/R (China)": 19.00,
        "A110X - Stainless Steel Hinge - T31 (12mm & 13mm) : L/R (China)": 24.20,
        "A110XX - Stainless Steel Hinge - T51 (18mm) : L/R (China)": 22.10,
        "A118 - Stainless Steel Conceal Hinge (Local)": 10.00,
        "A113 - Stainless Steel Doric Hinge (China)": 9.50,
        "A110M - Stainless Steel Hinge - T21 (10mm) : L/R (Maghin)": 30.00,
        "A110MX - Stainless Steel Hinge - T31 (12/13mm) : L/R (Maghin)": 40.00,
        "A110MXX - Stainless Steel Hinge - T51 (18mm) : L/R (Maghin)": 60.00
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
        "HRO6100B - Aluminium Oval Headrail - Black : 6.1m": 99.00,
        "HRO6100NA - Aluminium Oval Headrail - N/A : 6.1m": 94.00,
        "HRSQ6100B - Aluminium Square Headrail - Black : 6.1m": 116.00,
        "HRSQ6100NA - Aluminium Square Headrail - N/A : 6.1m": 115.00,
        "HRT6100B - Aluminium Triangle Headrail - Black : 6.1m": 75.00,
        "HRT6100NA - Aluminium Triangle Headrail - N/A : 6.1m": 76.00
    },
    "Door Frames": {
        "None": 0.00,
        "DFO4200B - Aluminium Door Frame (Old) + Angle - Black : 4.2m": 137.00,
        "DFO4200NA - Aluminium Door Frame (Old) + Angle - N/A : 4.2m": 125.00,
        "DFN4200B - Aluminium Door Frame (New) + Angle - Black : 4.2m": 100.00,
        "DFN4200NA - Aluminium Door Frame (New) + Angle - N/A : 4.2m": 98.00,
        "DFO4200GHB - Aluminium Door Frame (Old) c/w Gear Hinge - Black : 4.2m": 154.00,
        "DFO4200GHNA - Aluminium Door Frame (Old) c/w Gear Hinge - N/A : 4.2m": 141.00
    }
}

# Flatten prices for easy BOM lookup
FLAT_PRICES = {}
for category in ACCESSORIES_DB.values():
    FLAT_PRICES.update(category)

# Transport Database 
TRANSPORT_DB = {
    "Kuala Lumpur": {"1 Tonne": 120, "3 Tonne": 195},
    "Petaling Jaya": {"1 Tonne": 120, "3 Tonne": 195},
    "Shah Alam": {"1 Tonne": 135, "3 Tonne": 210},
    "Balakong": {"1 Tonne": 135, "3 Tonne": 210},
    "Serdang": {"1 Tonne": 135, "3 Tonne": 210},
    "Ampang": {"1 Tonne": 125, "3 Tonne": 200},
    "Bukit Indah": {"1 Tonne": 125, "3 Tonne": 200},
    "Pandan Indah": {"1 Tonne": 125, "3 Tonne": 200},
    "Cheras": {"1 Tonne": 125, "3 Tonne": 200},
    "Puchong": {"1 Tonne": 125, "3 Tonne": 200},
    "Kajang": {"1 Tonne": 175, "3 Tonne": 235},
    "Bangi": {"1 Tonne": 175, "3 Tonne": 235},
    "Putrajaya": {"1 Tonne": 175, "3 Tonne": 235},
    "Semenyih": {"1 Tonne": 185, "3 Tonne": 265},
    "Beranang": {"1 Tonne": 185, "3 Tonne": 265},
    "Nilai Industrial Area": {"1 Tonne": 225, "3 Tonne": 295},
    "Sepang & KLIA": {"1 Tonne": 240, "3 Tonne": 315},
    "Port Dickson": {"1 Tonne": 410, "3 Tonne": 500},
    "Bukit China": {"1 Tonne": 410, "3 Tonne": 500},
    "Klang": {"1 Tonne": 155, "3 Tonne": 235},
    "Port Klang": {"1 Tonne": 170, "3 Tonne": 245},
    "Port Klang Telok Gong": {"1 Tonne": 200, "3 Tonne": 255},
    "Pulau Indah, Klang": {"1 Tonne": 235, "3 Tonne": 305},
    "West Port Klang": {"1 Tonne": 235, "3 Tonne": 305},
    "Kuala Langat": {"1 Tonne": 235, "3 Tonne": 305},
    "Banting": {"1 Tonne": 235, "3 Tonne": 305},
    "Senawang": {"1 Tonne": 290, "3 Tonne": 360},
    "Seremban": {"1 Tonne": 290, "3 Tonne": 360},
    "Rembau": {"1 Tonne": 350, "3 Tonne": 450},
    "Jelebu": {"1 Tonne": 350, "3 Tonne": 450},
    "Melaka": {"1 Tonne": 510, "3 Tonne": 640},
    "Muar": {"1 Tonne": 610, "3 Tonne": 780},
    "Yong Peng": {"1 Tonne": 610, "3 Tonne": 780},
    "Segamat": {"1 Tonne": 610, "3 Tonne": 780},
    "Batu Pahat": {"1 Tonne": 610, "3 Tonne": 780},
    "Ayer Hitam": {"1 Tonne": 780, "3 Tonne": 980},
    "Machap": {"1 Tonne": 780, "3 Tonne": 980},
    "Johor Bahru": {"1 Tonne": 780, "3 Tonne": 980},
    "Mersing": {"1 Tonne": 980, "3 Tonne": 1150},
    "Lembah Beringin till Tg M": {"1 Tonne": 290, "3 Tonne": 350},
    "Bidor till Tapah": {"1 Tonne": 480, "3 Tonne": 600},
    "Kampar till Ipoh": {"1 Tonne": 570, "3 Tonne": 720},
    "Sri Manjung": {"1 Tonne": 660, "3 Tonne": 810},
    "Lumut": {"1 Tonne": 660, "3 Tonne": 810},
    "Batang Kali": {"1 Tonne": 220, "3 Tonne": 290},
    "Kuala Kangsar": {"1 Tonne": 630, "3 Tonne": 800},
    "Taiping": {"1 Tonne": 680, "3 Tonne": 850},
    "Sg Rengit": {"1 Tonne": 1200, "3 Tonne": 1500},
    "Pengerang": {"1 Tonne": 1200, "3 Tonne": 1500},
    "Desaru": {"1 Tonne": 1200, "3 Tonne": 1500},
    "Pantai Remis": {"1 Tonne": 770, "3 Tonne": 950},
    "Pulau Pinang": {"1 Tonne": 790, "3 Tonne": 980},
    "Teluk Bahang till Balik Pu": {"1 Tonne": 830, "3 Tonne": 1030},
    "Kulim": {"1 Tonne": 850, "3 Tonne": 1050},
    "Sungai Petani": {"1 Tonne": 850, "3 Tonne": 1050},
    "Gurun Till Bedong": {"1 Tonne": 850, "3 Tonne": 1050},
    "Baling": {"1 Tonne": 980, "3 Tonne": 1200},
    "Keroh": {"1 Tonne": 980, "3 Tonne": 1200},
    "Langkawi Port/Jetty": {"1 Tonne": 980, "3 Tonne": 1200},
    "Alor Setar": {"1 Tonne": 980, "3 Tonne": 1200},
    "Kangar": {"1 Tonne": 1070, "3 Tonne": 1300},
    "Padang Besar": {"1 Tonne": 1070, "3 Tonne": 1300},
    "Bukit Kayu Hitam": {"1 Tonne": 1070, "3 Tonne": 1300},
    "Perlis": {"1 Tonne": 1070, "3 Tonne": 1300},
    "Genting Highlands till Ben": {"1 Tonne": 380, "3 Tonne": 470},
    "Mentakab till Temerloh": {"1 Tonne": 520, "3 Tonne": 660},
    "Maran": {"1 Tonne": 570, "3 Tonne": 730},
    "Kuantan Port till Pekan": {"1 Tonne": 680, "3 Tonne": 860},
    "Kuala Rompin": {"1 Tonne": 920, "3 Tonne": 1150},
    "Kemaman till Kerteh": {"1 Tonne": 800, "3 Tonne": 1000},
    "Dungun": {"1 Tonne": 870, "3 Tonne": 1070},
    "Terengganu Town": {"1 Tonne": 1100, "3 Tonne": 1350},
    "Kuala Berang": {"1 Tonne": 1100, "3 Tonne": 1350},
    "Besut till Jertih": {"1 Tonne": 1300, "3 Tonne": 1450},
    "Kota Bharu": {"1 Tonne": 1350, "3 Tonne": 1600},
    "Pasir Puteh till Pasir Mas": {"1 Tonne": 1350, "3 Tonne": 1600},
    "Tanah Merah Till Rantau": {"1 Tonne": 1350, "3 Tonne": 1650}
}

# Labor Database (Compiled dynamically from Master Tiers)
LABOR_DB = {}
labor_groups = [
    (["KL & PJ"], 100, [120, 125, 125, 165], [137, 144, 144, 186], [0, 200, 200, 245], [96, 101, 101, 135], [83, 90, 90, 125]),
    (["Genting"], 150, [124, 130, 130, 170], [148, 154, 154, 200], [0, 206, 206, 250], [101, 107, 107, 140], [90, 96, 96, 130]),
    (["Shah Alam", "Klang", "Putrajaya", "UPM", "Bangi", "Kajang"], 100, [124, 130, 130, 170], [148, 154, 154, 200], [0, 206, 206, 250], [101, 107, 107, 140], [90, 96, 96, 130]),
    (["Seremban", "Ipoh", "Melaka"], 150, [136, 143, 143, 180], [161, 168, 168, 210], [0, 212, 212, 260], [107, 113, 113, 145], [96, 101, 101, 135]),
    (["Kuantan", "Pahang", "Penang", "Johor Bahru", "Taiping"], 150, [143, 148, 148, 190], [166, 174, 174, 216], [0, 217, 217, 265], [113, 120, 120, 151], [101, 107, 107, 140]),
    (["Terengganu", "Kelantan", "Perlis", "Kedah"], 200, [150, 155, 155, 200], [181, 188, 188, 230], [0, 238, 238, 270], [120, 125, 125, 160], [107, 113, 113, 145])
]

# Generate matrix automatically
for locs, meas, scan, orient, monitor, tech3, tech1 in labor_groups:
    for loc in locs:
        LABOR_DB[loc] = {
            "Scan": {"10mm": [meas, scan[0]], "12mm": [meas, scan[1]], "13mm": [meas, scan[2]], "18mm": [meas, scan[3]]},
            "Orient": {"10mm": [meas, orient[0]], "12mm": [meas, orient[1]], "13mm": [meas, orient[2]], "18mm": [meas, orient[3]]},
            "Monitor": {"10mm": [meas, monitor[0]], "12mm": [meas, monitor[1]], "13mm": [meas, monitor[2]], "18mm": [meas, monitor[3]]},
            "Tech 3": {"10mm": [meas, tech3[0]], "12mm": [meas, tech3[1]], "13mm": [meas, tech3[2]], "18mm": [meas, tech3[3]]},
            "Tech 1": {"10mm": [meas, tech1[0]], "12mm": [meas, tech1[1]], "13mm": [meas, tech1[2]], "18mm": [meas, tech1[3]]}
        }

# --- 2. STREAMLIT UI SETUP ---
st.set_page_config(page_title="Cubicle Costing App", layout="wide")
st.title("Full-Fledged Cubicle Costing & Optimization App")

st.sidebar.header("1. Project Settings")
sys_series = st.sidebar.selectbox("System Series", ["Scan", "Orient", "Monitor", "Tech 1", "Tech 3"])
brand = st.sidebar.selectbox("Board Brand", ["ASUWARIS", "Formica"])
finish = st.sidebar.selectbox("Finish Type", ["Solid", "Woodgrain"])
thickness = st.sidebar.selectbox("Thickness", ["10mm", "12mm", "13mm", "18mm"])
opt_mode = st.sidebar.radio("Board Stock Optimization", ["Ex-Stock (6x14 Only)", "All Stocks (Cost-Efficient)"])

st.sidebar.header("2. Hardware Configuration")
leg_type = st.sidebar.selectbox("Adjustable Leg", list(ACCESSORIES_DB["Legs"].keys()))
hook_type = st.sidebar.selectbox("Coat Hook", list(ACCESSORIES_DB["Hooks"].keys()))
knob_type = st.sidebar.selectbox("Door Knob", list(ACCESSORIES_DB["Door Knobs"].keys()))
lock_type = st.sidebar.selectbox("Lockset", list(ACCESSORIES_DB["Locksets"].keys()))
hinge_type = st.sidebar.selectbox("Hinge", list(ACCESSORIES_DB["Hinges"].keys()))
conn_type = st.sidebar.radio("Connector Style", ["L-Bracket", "U-Channel"])
lb_type = st.sidebar.selectbox("L-Bracket Type", list(ACCESSORIES_DB["L-Brackets"].keys()))
uc_type = st.sidebar.selectbox("U-Channel Type", list(ACCESSORIES_DB["U-Channels"].keys()))
hr_type = st.sidebar.selectbox("Headrail Type", list(ACCESSORIES_DB["Headrails"].keys()))
df_type = st.sidebar.selectbox("Door Frame (Tech 1)", list(ACCESSORIES_DB["Door Frames"].keys()))

st.sidebar.header("3. Logistics & Labor")
area = st.sidebar.selectbox("Project Area (Labor)", list(LABOR_DB.keys()))
transport_loc = st.sidebar.selectbox("Transport Destination", list(TRANSPORT_DB.keys()))
lorry_type = st.sidebar.radio("Lorry Size", ["1 Tonne", "3 Tonne"])

st.markdown("### Panel Dimensions & Quantities (mm)")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    door_w = st.number_input("Door W", value=600)
    door_h = st.number_input("Door H", value=1800)
    door_qty = st.number_input("Door Qty", value=0, min_value=0)

with col2:
    int_pil_w = st.number_input("Int Pilaster W", value=300)
    int_pil_h = st.number_input("Int Pilaster H", value=1800)
    int_pil_qty = st.number_input("Int Pil Qty", value=0, min_value=0)

with col3:
    end_pil_w = st.number_input("End Pilaster W", value=150)
    end_pil_h = st.number_input("End Pilaster H", value=1800)
    end_pil_qty = st.number_input("End Pil Qty", value=0, min_value=0)

with col4:
    div_pan_w = st.number_input("Div Panel W", value=1500)
    div_pan_h = st.number_input("Div Panel H", value=1800)
    div_pan_qty = st.number_input("Div Panel Qty", value=0, min_value=0)

with col5:
    uri_pan_w = st.number_input("Urinal W", value=450)
    uri_pan_h = st.number_input("Urinal H", value=900)
    uri_pan_qty = st.number_input("Urinal Qty", value=0, min_value=0)

# --- 3. CORE CALCULATION ENGINE ---
if st.button("Calculate Total Project Cost", type="primary"):
    bom = {}
    hw_cost = 0

    # Door Hardware
    hinges_per_door = 4 if door_h > 2100 else 3
    if door_qty > 0:
        if hinge_type != "None": bom[hinge_type] = door_qty * hinges_per_door
        if hook_type != "None": bom[hook_type] = door_qty * 1
        if knob_type != "None": bom[knob_type] = door_qty * 1
        if lock_type != "None": bom[lock_type] = door_qty * 1
    
    # Adjustable Legs
    if sys_series == "Scan" and leg_type != "None":
        total_legs = (int_pil_qty * 2) + (end_pil_qty * 1)
        if total_legs > 0: bom[leg_type] = total_legs

    # Connectors
    if conn_type == "L-Bracket":
        total_brackets = (div_pan_qty * (8 if div_pan_h > 2100 else 6)) + \
                         (int_pil_qty * (8 if int_pil_h > 2100 else 6)) + \
                         (end_pil_qty * (4 if end_pil_h > 2100 else 3)) + \
                         (uri_pan_qty * 6)
        if total_brackets > 0 and lb_type != "None": bom[lb_type] = total_brackets
    else:
        total_u_mm = (div_pan_qty * div_pan_h) + (int_pil_qty * int_pil_h) + (end_pil_qty * end_pil_h)
        if total_u_mm > 0 and uc_type != "None": bom[uc_type] = math.ceil(total_u_mm / 6100)
        if uri_pan_qty > 0 and lb_type != "None": bom[lb_type] = (uri_pan_qty * 6)

    # Headrail & Extrusions
    if sys_series in ["Scan", "Orient"] and hr_type != "None":
        hr_length = ((door_qty * door_w) + (int_pil_qty * int_pil_w) + (end_pil_qty * end_pil_w)) * 1.10
        if hr_length > 0: bom[hr_type] = math.ceil(hr_length / 6100)
        
    if sys_series == "Tech 1" and door_qty > 0 and df_type != "None":
        frame_mm = door_qty * ((door_h * 2) + door_w)
        bom[df_type] = math.ceil(frame_mm / 4200)

    # Nesting & Board Cost 
    kerf = 5
    total_area = (door_qty * (door_w + kerf) * (door_h + kerf)) + \
                 (int_pil_qty * (int_pil_w + kerf) * (int_pil_h + kerf)) + \
                 (end_pil_qty * (end_pil_w + kerf) * (end_pil_h + kerf)) + \
                 (uri_pan_qty * (uri_pan_w + kerf) * (uri_pan_h + kerf))
                 
    if sys_series not in ["Tech 1", "Tech 3"]:
        total_area += (div_pan_qty * (div_pan_w + kerf) * (div_pan_h + kerf))

    price_dict = ASUWARIS_PRICES[finish] if brand == "ASUWARIS" else FORMICA_PRICES[finish]
    used_boards = {}
    board_cost = 0
    
    if total_area > 0:
        if opt_mode == "Ex-Stock (6x14 Only)":
            b_name = "6x14"
            a_b = BOARD_DIMS[b_name][0] * BOARD_DIMS[b_name][1] * 0.85
            qty = math.ceil(total_area / a_b)
            used_boards[b_name] = qty
            board_cost = qty * price_dict[b_name]
        else:
            # All Stocks Optimization Heuristic
            sizes = ["6x14", "6x12", "6x8"] if brand == "ASUWARIS" else ["6x14", "6x12", "6x9"]
            s14, s12, sSmall = sizes[0], sizes[1], sizes[2]
            
            a14 = BOARD_DIMS[s14][0] * BOARD_DIMS[s14][1] * 0.85
            a12 = BOARD_DIMS[s12][0] * BOARD_DIMS[s12][1] * 0.85
            aSmall = BOARD_DIMS[sSmall][0] * BOARD_DIMS[sSmall][1] * 0.85
            
            p14 = price_dict[s14]
            p12 = price_dict[s12]
            pSmall = price_dict[sSmall]
            
            max_14 = math.ceil(total_area / a14) + 1
            max_12 = math.ceil(total_area / a12) + 1
            
            best_cost = float('inf')
            best_combo = {}
            
            for n_14 in range(max_14):
                for n_12 in range(max_12):
                    covered = (n_14 * a14) + (n_12 * a12)
                    if covered >= total_area:
                        n_small = 0
                    else:
                        n_small = math.ceil((total_area - covered) / aSmall)
                    
                    cost = (n_14 * p14) + (n_12 * p12) + (n_small * pSmall)
                    if cost < best_cost:
                        best_cost = cost
                        best_combo = {s14: n_14, s12: n_12, sSmall: n_small}
                        
            used_boards = {k: v for k, v in best_combo.items() if v > 0}
            board_cost = best_cost

    # Compile Itemized Materials Table
    itemized_data = []
    
    for item, qty in bom.items():
        unit_price = FLAT_PRICES.get(item, 0)
        total_item_cost = unit_price * qty
        hw_cost += total_item_cost
        itemized_data.append({
            "Item": item,
            "Qty": qty,
            "Unit Price (RM)": f"{unit_price:,.2f}",
            "Total Cost (RM)": f"{total_item_cost:,.2f}"
        })
        
    for b_size, qty in used_boards.items():
        unit_price = price_dict[b_size]
        itemized_data.append({
            "Item": f"Raw Board ({brand} {finish} {b_size})",
            "Qty": qty,
            "Unit Price (RM)": f"{unit_price:,.2f}",
            "Total Cost (RM)": f"{qty * unit_price:,.2f}"
        })

    # Labor Cost Calculation
    labor_cost = 0
    measurement_cost = 0
    try:
        rates = LABOR_DB[area][sys_series][thickness]
        measurement_cost = rates[0]
        labor_cost = (rates[1] * door_qty) + measurement_cost 
    except KeyError:
        st.warning("Labor rates for this specific Area/Series/Thickness combination are not in the sample DB yet.")

    # Transport Cost Calculation
    transport_cost = TRANSPORT_DB[transport_loc][lorry_type]

    # --- 4. RESULTS RENDER ---
    st.markdown("---")
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.subheader("Materials Breakdown")
        
        if used_boards:
            st.write("**Boards Needed:**")
            for b_size, qty in used_boards.items():
                st.write(f"- {qty}x ({b_size})")
                
        if itemized_data:
            st.table(pd.DataFrame(itemized_data))
        st.metric("Total Material Cost", f"RM {hw_cost + board_cost:,.2f}")

    with c2:
        st.subheader("Project Summary")
        
        st.write(f"**Transport Destination:** {transport_loc} ({lorry_type})")
        st.metric("Transportation Cost", f"RM {transport_cost:,.2f}")
        
        st.write(f"**Labor Area:** {area}")
        st.write(f"*(Includes Measurement Fee: RM {measurement_cost:,.2f})*")
        st.metric("Total Labor Cost", f"RM {labor_cost:,.2f}")
        
        st.markdown("---")
        st.subheader("Final Project Cost")
        grand_total = hw_cost + board_cost + transport_cost + labor_cost
        st.metric("Grand Total (RM)", f"RM {grand_total:,.2f}")
        
        if door_qty > 0:
            st.write(f"**Estimated Cost per Cubicle:** RM {grand_total / door_qty:,.2f}")
