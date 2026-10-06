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
    "Shah Alam": {"1 Tonne": 135, "3 Tonne": 210},
    "Klang": {"1 Tonne": 155, "3 Tonne": 235},
    "Seremban": {"1 Tonne": 290, "3 Tonne": 360},
    "Melaka": {"1 Tonne": 510, "3 Tonne": 640},
    "Johor Bahru": {"1 Tonne": 780, "3 Tonne": 980},
    "Kuantan Port till Pekan": {"1 Tonne": 680, "3 Tonne": 860},
    "Penang": {"1 Tonne": 790, "3 Tonne": 980}
}

# Labor Database 
LABOR_DB = {
    "KL & PJ": {
        "Scan": {"10mm": [100, 120], "12mm": [100, 125], "13mm": [100, 125], "18mm": [100, 165]},
        "Orient": {"10mm": [100, 137], "12mm": [100, 144], "13mm": [100, 144], "18mm": [100, 186]},
        "Monitor": {"10mm": [100, 200], "12mm": [100, 200], "13mm": [100, 200], "18mm": [100, 245]},
        "Tech 1": {"10mm": [100, 83], "12mm": [100, 90], "13mm": [100, 90], "18mm": [100, 125]},
        "Tech 3": {"10mm": [100, 96], "12mm": [100, 101], "13mm": [100, 101], "18mm": [100, 135]}
    },
    "Shah Alam": {
        "Scan": {"12mm": [100, 130]}, 
        "Tech 1": {"12mm": [100, 85]}
    }
}

# --- 2. STREAMLIT UI SETUP ---
st.set_page_config(page_title="Cubicle Costing App", layout="wide")
st.title("Full-Fledged Cubicle Costing & Optimization App")

st.sidebar.header("1. Project Settings")
sys_series = st.sidebar.selectbox("System Series", ["Scan", "Orient", "Monitor", "Tech 1", "Tech 3"])
brand = st.sidebar.selectbox("Board Brand", ["ASUWARIS", "Formica"])
finish = st.sidebar.selectbox("Finish Type", ["Solid", "Woodgrain"])
thickness = st.sidebar.selectbox("Thickness", ["10mm", "12mm", "13mm", "18mm"])

st.sidebar.header("2. Hardware Configuration")
leg_type = st.sidebar.selectbox("Adjustable Leg", list(ACCESSORIES_DB["Legs"].keys()))
hook_type = st.sidebar.selectbox("Coat Hook", list(ACCESSORIES_DB["Hooks"].keys()))
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

    # Nesting & Board Cost (Simplified Area Heuristic)
    kerf = 5
    total_area = (door_qty * (door_w + kerf) * (door_h + kerf)) + \
                 (int_pil_qty * (int_pil_w + kerf) * (int_pil_h + kerf)) + \
                 (end_pil_qty * (end_pil_w + kerf) * (end_pil_h + kerf)) + \
                 (uri_pan_qty * (uri_pan_w + kerf) * (uri_pan_h + kerf))
                 
    if sys_series not in ["Tech 1", "Tech 3"]:
        total_area += (div_pan_qty * (div_pan_w + kerf) * (div_pan_h + kerf))

    b_area = 1830 * 4270 
    boards_needed = math.ceil(total_area / (b_area * 0.85)) if total_area > 0 else 0
    
    price_dict = ASUWARIS_PRICES[finish] if brand == "ASUWARIS" else FORMICA_PRICES[finish]
    board_unit_price = price_dict.get("6x14", 0)
    board_cost = boards_needed * board_unit_price

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
        
    if boards_needed > 0:
        itemized_data.append({
            "Item": f"Raw Board ({brand} {finish} 6x14)",
            "Qty": boards_needed,
            "Unit Price (RM)": f"{board_unit_price:,.2f}",
            "Total Cost (RM)": f"{board_cost:,.2f}"
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
        if itemized_data:
            st.table(pd.DataFrame(itemized_data))
        st.metric("Total Material Cost", f"RM {hw_cost + board_cost:,.2f}")

    with c2:
        st.subheader("Logistics & Labor")
        st.write(f"**Location:** {transport_loc} ({lorry_type})")
        st.write(f"**Area (Labor):** {area}")
        st.write(f"**Measurement Fee:** RM {measurement_cost:,.2f}")
        st.metric("Total Logistics Cost", f"RM {transport_cost + labor_cost:,.2f}")
        
        st.markdown("---")
        st.subheader("Final Project Cost")
        grand_total = hw_cost + board_cost + transport_cost + labor_cost
        st.metric("Grand Total (RM)", f"RM {grand_total:,.2f}")
        if door_qty > 0:
            st.write(f"**Estimated Cost per Cubicle:** RM {grand_total / door_qty:,.2f}")
