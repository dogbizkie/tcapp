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

# Categorized Accessory Database (Mapped from master list)
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
        "A127 - Stainless Steel L-Bracket (2\" x 2\") China": 3.00,
        "A127x - Stainless Steel L-Bracket (2\" x 3\") Asuwaris": 3.00
    },
    "U-Channels": {
        "None": 0.00,
        "106100B - Aluminium U-Channel - Black : 6.1m (10mm)": 36.50,
        "106100NA - Aluminium U-Channel - N
