import streamlit as st 
import random

st.title("UE Type Generator (Fixed Template + Key Params Only)")

# =========================================================
# 1. TEMPLATE
# =========================================================
def load_template(ue_type):

    base = {
        "mcs_table": "qam256",
        "imcs": 15,
        "dmrs": 2,
        "rb_len": 2,
        "rb_offset": 1,
        "sym_offset": 0,
        "sym_length": 14,
        "channel": 9,
        "delay": 10,
        "speed": 30,
        "cfo": 500,
        "rnti": 17017,
        "l0": 2
    }

    if ue_type == "TYPE0":
        base.update({
            "imcs": 15,
            "dmrs": 2,
            "rb_len": 2,
            "rb_offset": 1,
            "sym_offset": 0,
            "sym_length": 14,
            "cfo": 500,
            "rnti": 17017,
            "l0": 2
        })

    elif ue_type == "TYPE1":
        base.update({
            "imcs": 5,
            "dmrs": 1,
            "rb_len": 3,
            "rb_offset": 5,
            "sym_offset": 0,
            "sym_length": 5,
            "cfo": 800,
            "rnti": 1,
            "l0": 3
        })

    return base


# =========================================================
# 2. TYPE SELECT
# =========================================================
ue_type = st.selectbox("UE Type", ["TYPE0", "TYPE1"])

cfg = load_template(ue_type)

# =========================================================
# 3. ONLY KEY PARAMETERS
# =========================================================
st.subheader("Editable Parameters")

mcs_table = st.selectbox(
    "MCS Table",
    ["qam64", "qam256"],
    index=["qam64", "qam256"].index(cfg["mcs_table"])
)

imcs = st.number_input("MCS (Imcs)", 0, 27, cfg["imcs"])

dmrs = st.number_input(
    "DMRSNUM (AdditionalPosition + 1)",
    1,
    4,
    cfg["dmrs"]
)

rb_len = st.number_input(
    "RBLength (nPRB)",
    1,
    273,
    cfg["rb_len"]
)

rb_offset = st.number_input(
    "RB Offset",
    0,
    273,
    cfg["rb_offset"]
)

sym_offset = st.number_input(
    "symstr (Symbol Offset)",
    0,
    4,
    cfg["sym_offset"]
)

sym_length = st.number_input(
    "symlength",
    1,
    14,
    cfg["sym_length"]
)

l0 = st.selectbox(
    "DMRS l0",
    [2, 3],
    index=[2, 3].index(cfg["l0"])
)

# =========================================================
# 4. FIXED PARAMETERS
# =========================================================
channel = cfg["channel"]
delay = cfg["delay"]
speed = cfg["speed"]
rnti = cfg["rnti"]

# =========================================================
# 5. CFO RULE
# =========================================================
# DMRS=1 -> random 10~30
# TYPE0 -> 500
# TYPE1 -> 800
if dmrs == 1 and ue_type == "TYPE1":
    # cfo = random.randint(10, 30)
    cfo = 23
elif dmrs == 1 and ue_type == "TYPE0":
    cfo = 27
else:
    cfo = cfg["cfo"]

# =========================================================
# 6. GENERATE TEXT
# =========================================================
txt = f"""//(--Antenna Config--)
NUEAnt 1
NMaxlayer 1
PrecodingType SVD
FixPMI 1

//(--Channel Config--)
channelidx {channel}
DelaySpread {delay}
UserSpeed {speed}
STOvalue 36
CFOvalue {cfo}

//(--PDSCH,PUSCH--)
symOffset {sym_offset}
symLength {sym_length}
rbOffset {rb_offset}
nPRB {rb_len}
RNTI {rnti}
harqFlag 1
rv 0

//(--MCS--)
mcsTable {mcs_table}
Imcs {imcs}

//(--DMRS--)
configType 1
cdm 2
dmrslength 1
l0 {l0}
l1 11
AdditionalPosition {dmrs - 1}

//(--LDPC Config--)
MaximumLDPCIterationCount 63

//(--PRACH--)
PreambleIndex 23
TimeErrorTolerance 0
"""

# =========================================================
# 7. OUTPUT
# =========================================================
st.subheader("UE_Type.txt Preview")

st.text_area(
    "",
    txt,
    height=450
)

st.download_button(
    "Download UE_Type.txt",
    txt,
    file_name=f"UE_{ue_type}.txt"
)     