import streamlit as st

st.title("Verilog Slot Generator")



# =========================================================
# Input Text
# =========================================================
st.subheader("Input")

input_text = st.text_area(
    "Paste Verilog / Text here",
    height=300
)

# =========================================================
# Replace Rules
# =========================================================
st.subheader("Replace Rules")

default_rules = [
    ("_SlotIdx0", "_SlotIdx{slot}"),
    ("_SLOT0", "_SLOT{slot}"),
    ("_slot0", "_slot{slot}")
]

num_rules = st.number_input(
    "Number of patterns",
    min_value=1,
    max_value=20,
    value=len(default_rules)
)

rules = []

for i in range(num_rules):

    default_src = ""
    default_dst = ""

    if i < len(default_rules):
        default_src = default_rules[i][0]
        default_dst = default_rules[i][1]

    col1, col2 = st.columns(2)

    with col1:
        src = st.text_input(
            f"Find {i}",
            value=default_src,
            key=f"find_{i}"
        )

    with col2:
        dst = st.text_input(
            f"Replace {i}",
            value=default_dst,
            key=f"replace_{i}"
        )

    rules.append((src, dst))
# =========================================================
# Slot Settings
# =========================================================
st.subheader("Slot Settings")

view_mode = st.radio(
    "View Mode",
    ["All Slots", "Single Slot"],
    horizontal=True
)

slot_max = st.number_input(
    "Max Slot (0~N)",
    min_value=0,
    max_value=100,
    value=9
)

single_slot = st.number_input(
    "Select Slot",
    min_value=0,
    max_value=slot_max,
    value=0
)
# =====================================================
# Auto Generate
# =====================================================

if input_text.strip():

    output_all = ""

    # All Slots
    if view_mode == "All Slots":

        for slot in range(slot_max + 1):

            new_txt = input_text

            for src, dst in rules:

                if src.strip():
                    new_txt = new_txt.replace(
                        src,
                        dst.format(slot=slot)
                    )

            output_all += new_txt + "\n"

    # Single Slot
    else:

        slot = single_slot

        new_txt = input_text

        for src, dst in rules:

            if src.strip():
                new_txt = new_txt.replace(
                    src,
                    dst.format(slot=slot)
                )

        output_all = new_txt

    st.subheader("Result")

    st.code(
        output_all,
        language="verilog"
    )

else:
    st.info("Paste Verilog / Text here")