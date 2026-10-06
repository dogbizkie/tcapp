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
    "Door Jambs": {
        "None": 0.00,
        "10DJB6100 - Aluminium Door Jamb - Black : 6.1m (10mm)": 23.50,
        "10DJNA6100 - Aluminium Door Jamb - N/A : 6.1m (10mm)": 21.00,
        "12DJB6100 - Aluminium Door Jamb - Black : 6.1m (12 & 13mm)": 26.00,
        "12DJNA6100 - Aluminium Door Jamb - N/A : 6.1m (12 & 13mm)": 22.00,
        "18DJB6100 - Aluminium Door Jamb - Black : 6.1m (18mm)": 33.00,
        "18DJNA6100 - Aluminium Door Jamb - N/A : 6.1m (18mm)": 27.00
    },
    "Door Frames": {
        "None": 0.00,
        "DFO4200B - Aluminium Door Frame (Old) + Angle - Black : 4.2m": 137.00,
        "DFO4200NA - Aluminium Door Frame (Old) + Angle - N/A : 4.2m": 125.00,
        "DFN4200B - Aluminium Door Frame (New) + Angle - Black : 4.2m": 100.00,
        "DFN4200NA - Aluminium Door Frame (New) + Angle - N/A : 4.2m": 98.00,
        "DFO4200GHB - Aluminium Door Frame (Old) c/w Gear Hinge - Black : 4.2m": 154.00,
        "DFO4200GHNA - Aluminium Door Frame (Old) c/w Gear Hinge - N/A : 4.2m": 141.00
    },
    "Aluminium Profiles": {
        "None": 0.00,
        "CRNR6100B - Aluminium Corner - Black : 6.1m": 62.00,
        "CRNR6100NA - Aluminium Corner - N/A : 6.1m": 56.00,
        "SQPOLE6100B - Aluminium Square Pole - Black : 6.1m": 98.00,
        "SQPOLE6100NA - Aluminium Square Pole - N/A : 6.1m": 94.50,
        "AGH4000B - Aluminium Gear Hinge - Black : 4.0m": 77.00,
        "AGH4000NA - Aluminium Gear Hinge - N/A : 4.0m": 74.00,
        'LANGLE1X26100B - Aluminium L-Angle (1" x 2") - Black : 6.1m': 53.00,
        'LANGLE1X26100NA - Aluminium L-Angle (1" x 2") - N/A : 6.1m': 46.50,
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
    "Shoeboxes": {
        "None": 0.00,
        "ASB6100B - Aluminium Shoe Box + Angle - Black : 6.1m": 94.00,
        "ASB6100NA - Aluminium Shoe Box + Angle - N/A : 6.1m": 85.50,
        "ASBCAPPING - Aluminium Shoe Capping (Black & Grey)": 1.75,
        "SS100 - Size 100mm x 100mm (L)": 13.50,
        "SS200 - Size 100mm x 200mm (L)": 21.00,
        "SS300 - Size 100mm x 300mm (L)": 26.00,
        "SS400 - Size 100mm x 400mm (L)": 31.00,
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

# Labor Database
LABOR_DB = {}
labor_groups = [
    (["KL & PJ"], 100, [120, 125, 125, 165], [137, 144, 144, 186], [0, 200, 200, 245], [96, 101, 101, 135], [83, 90, 90, 125]),
    (["Genting"], 150, [124, 130, 130, 170], [148, 154, 154, 200], [0, 206, 206, 250], [101, 107, 107, 140], [90, 96, 96, 130]),
    (["Shah Alam", "Klang", "Putrajaya", "UPM", "Bangi", "Kajang"], 100, [124, 130, 130, 170], [148, 154, 154, 200], [0, 206, 206, 250], [101, 107, 107, 140], [90, 96, 96, 130]),
    (["Seremban", "Ipoh", "Melaka"], 150, [136, 143, 143, 180], [161, 168, 168, 210], [0, 212, 212, 260], [107, 113, 113, 145], [96, 101, 101, 135]),
    (["Kuantan", "Pahang", "Penang", "Johor Bahru", "Taiping"], 150, [143, 148, 148, 190], [166, 174, 174, 216], [0, 217, 217, 265], [113, 120, 120, 151], [101, 107, 107, 140]),
    (["Terengganu", "Kelantan", "Perlis", "Kedah"], 200, [150, 155, 155, 200], [181, 188, 188, 230], [0, 238, 238, 270], [120, 125, 125, 160], [107, 113, 113, 145])
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

# --- INITIALIZE STATE ---
if 'calc_run' not in st.session_state:
    st.session_state.calc_run = False

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
df_type = st.sidebar.selectbox("Door Frame", list(ACCESSORIES_DB["Door Frames"].keys()))

st.sidebar.markdown("### Extra Extrusions & Hardware")
dj_type = st.sidebar.selectbox("Door Jamb", list(ACCESSORIES_DB["Door Jambs"].keys()))
dj_qty = st.sidebar.number_input("Door Jamb Qty", min_value=0, value=0)
ap_type = st.sidebar.selectbox("Aluminium Profile", list(ACCESSORIES_DB["Aluminium Profiles"].keys()))
ap_qty = st.sidebar.number_input("Profile Qty", min_value=0, value=0)
sb_type = st.sidebar.selectbox("Shoebox", list(ACCESSORIES_DB["Shoeboxes"].keys()))
sb_qty = st.sidebar.number_input("Shoebox Qty", min_value=0, value=0)

st.sidebar.header("3. Logistics & Labor")
area = st.sidebar.selectbox("Project Area (Labor)", list(LABOR_DB.keys()))
transport_loc = st.sidebar.selectbox("Transport Destination", list(TRANSPORT_DB.keys()))
lorry_type = st.sidebar.radio("Lorry Size", ["1 Tonne", "3 Tonne"])

st.markdown("### Panel Dimensions & Quantities (mm)")
st.info("Edit the table to change sizes, or click the **'+' button** at the bottom of a table to add a new row for custom sizes.")

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


# --- Helper to parse data editor tables safely ---
def get_clean_rows(df):
    rows = []
    for _, row in df.iterrows():
        try:
            qty = int(row.get('Qty', 0))
            w = float(row.get('Width', 0))
            h = float(row.get('Height', 0))
            if qty > 0:
                rows.append({"w": w, "h": h, "qty": qty})
        except (ValueError, TypeError):
            continue
    return rows


# --- 3. CORE CALCULATION ENGINE ---
if st.button("Calculate Total Project Cost", type="primary"):
    
    # Process all dynamic tables
    doors = get_clean_rows(df_doors)
    int_pils = get_clean_rows(df_int_pil)
    end_pils = get_clean_rows(df_end_pil)
    divs = get_clean_rows(df_div)
    end_divs = get_clean_rows(df_end_div)
    uris = get_clean_rows(df_uri)
    
    total_doors = sum(d['qty'] for d in doors)
    total_int_pil = sum(p['qty'] for p in int_pils)
    total_end_pil = sum(p['qty'] for p in end_pils)
    total_uri = sum(u['qty'] for u in uris)
    
    bom = {}

    # Door Hardware
    if total_doors > 0:
        hinge_count = sum(d['qty'] * (4 if d['h'] > 2100 else 3) for d in doors)
        if hinge_type != "None": bom[hinge_type] = hinge_count
        if hook_type != "None": bom[hook_type] = total_doors * 1
        if knob_type != "None": bom[knob_type] = total_doors * 1
        if lock_type != "None": bom[lock_type] = total_doors * 1
    
    # Adjustable Legs
    if sys_series == "Scan" and leg_type != "None":
        total_legs = (total_int_pil * 2) + (total_end_pil * 1)
        if total_legs > 0: bom[leg_type] = total_legs

    # Connectors
    lb_count = 0
    uc_mm = 0
    
    for item in divs + end_divs + int_pils:
        lb_count += item['qty'] * (8 if item['h'] > 2100 else 6)
        uc_mm += item['qty'] * item['h']
        
    for item in end_pils:
        lb_count += item['qty'] * (4 if item['h'] > 2100 else 3)
        uc_mm += item['qty'] * item['h']
        
    lb_count += total_uri * 6

    if conn_type == "L-Bracket":
        if lb_count > 0 and lb_type != "None": 
            bom[lb_type] = lb_count
    else:
        if uc_mm > 0 and uc_type != "None": 
            bom[uc_type] = math.ceil(uc_mm / 6100)
        if total_uri > 0 and lb_type != "None": 
            bom[lb_type] = (total_uri * 6)

    # Headrail
    if sys_series in ["Scan", "Orient"] and hr_type != "None":
        hr_front_width = sum(d['qty'] * d['w'] for d in doors) + \
                         sum(p['qty'] * p['w'] for p in int_pils) + \
                         sum(p['qty'] * p['w'] for p in end_pils)
        hr_length = hr_front_width * 1.10
        if hr_length > 0: bom[hr_type] = math.ceil(hr_length / 6100)
        
    # Door Frames
    if sys_series == "Tech 1" and total_doors > 0 and df_type != "None":
        frame_mm = sum(d['qty'] * ((d['h'] * 2) + d['w']) for d in doors)
        bom[df_type] = math.ceil(frame_mm / 4200)

    # Add custom extrusions/shoeboxes
    if dj_type != "None" and dj_qty > 0:
        bom[dj_type] = bom.get(dj_type, 0) + dj_qty
    if ap_type != "None" and ap_qty > 0:
        bom[ap_type] = bom.get(ap_type, 0) + ap_qty
    if sb_type != "None" and sb_qty > 0:
        bom[sb_type] = bom.get(sb_type, 0) + sb_qty

    # Nesting & Board Cost (With Kerf)
    kerf = 5
    total_area = 0
    
    for item in doors + int_pils + end_pils + uris:
        total_area += item['qty'] * (item['w'] + kerf) * (item['h'] + kerf)
        
    if sys_series not in ["Tech 1", "Tech 3"]:
        for item in divs + end_divs:
            total_area += item['qty'] * (item['w'] + kerf) * (item['h'] + kerf)

    price_dict = ASUWARIS_PRICES[finish] if brand == "ASUWARIS" else FORMICA_PRICES[finish]
    used_boards = {}
    
    if total_area > 0:
        if opt_mode == "Ex-Stock (6x14 Only)":
            b_name = "6x14"
            a_b = BOARD_DIMS[b_name][0] * BOARD_DIMS[b_name][1] * 0.85
            qty = math.ceil(total_area / a_b)
            used_boards[b_name] = qty
        else:
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

    # Compile Session Data for editable table
    bom_list = []
    for item, qty in bom.items():
        bom_list.append({"Item": item, "Unit Price (RM)": FLAT_PRICES.get(item, 0), "Qty": qty})
        
    for b_size, qty in used_boards.items():
        bom_list.append({"Item": f"Raw Board ({brand} {finish} {b_size})", "Unit Price (RM)": price_dict[b_size], "Qty": qty})

    # Labor Cost Calculation
    labor_cost = 0
    measurement_cost = 0
    try:
        rates = LABOR_DB[area][sys_series][thickness]
        measurement_cost = rates[0]
        labor_cost = (rates[1] * total_doors) + measurement_cost 
    except KeyError:
        st.warning("Labor rates for this specific Area/Series/Thickness combination are not in the sample DB yet.")

    # Save logic to session state
    st.session_state.bom_list = bom_list
    st.session_state.used_boards = used_boards
    st.session_state.labor_cost = labor_cost
    st.session_state.measurement_cost = measurement_cost
    st.session_state.transport_cost = TRANSPORT_DB[transport_loc][lorry_type]
    st.session_state.transport_loc = transport_loc
    st.session_state.lorry_type = lorry_type
    st.session_state.area = area
    st.session_state.total_doors = total_doors
    st.session_state.calc_run = True


# --- 4. RESULTS RENDER (Persists and updates automatically) ---
if st.session_state.calc_run:
    st.markdown("---")
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.subheader("Materials Breakdown")
        
        if st.session_state.used_boards:
            st.write("**Boards Needed (Initial Yield Calculation):**")
            for b_size, qty in st.session_state.used_boards.items():
                st.write(f"- {qty}x ({b_size})")
                
        st.write("*(You can manually adjust the **Qty** below. The grand totals on the right will update automatically.)*")
        
        # Interactive Editor
        df_bom = pd.DataFrame(st.session_state.bom_list)
        edited_bom = st.data_editor(
            df_bom,
            column_config={
                "Item": st.column_config.TextColumn("Item", disabled=True),
                "Unit Price (RM)": st.column_config.NumberColumn("Unit Price (RM)", format="%.2f", disabled=True),
                "Qty": st.column_config.NumberColumn("Qty", min_value=0, step=1)
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Recalculate dynamic material cost based on edited table
        edited_bom["Total Cost (RM)"] = edited_bom["Qty"] * edited_bom["Unit Price (RM)"]
        dynamic_material_cost = edited_bom["Total Cost (RM)"].sum()
        
        st.metric("Total Material Cost", f"RM {dynamic_material_cost:,.2f}")

    with c2:
        st.subheader("Project Summary")
        
        st.write(f"**Transport Destination:** {st.session_state.transport_loc} ({st.session_state.lorry_type})")
        st.metric("Transportation Cost", f"RM {st.session_state.transport_cost:,.2f}")
        
        st.write(f"**Labor Area:** {st.session_state.area}")
        st.write(f"*(Includes Measurement Fee: RM {st.session_state.measurement_cost:,.2f})*")
        st.metric("Total Labor Cost", f"RM {st.session_state.labor_cost:,.2f}")
        
        st.markdown("---")
        st.subheader("Final Project Cost")
        grand_total = dynamic_material_cost + st.session_state.transport_cost + st.session_state.labor_cost
        st.metric("Grand Total (RM)", f"RM {grand_total:,.2f}")
        
        if st.session_state.total_doors > 0:
            st.write(f"**Estimated Cost per Cubicle:** RM {grand_total / st.session_state.total_doors:,.2f}")
