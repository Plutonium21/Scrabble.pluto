import streamlit as st

st.set_page_config(layout="wide")

st.title("Scrabble Board Interaction Test")

if "selected" not in st.session_state:
    st.session_state.selected = None


def select_square(row, col):
    st.session_state.selected = (row, col)


st.write("Click any square below.")

# Column labels
header = st.columns([0.55] + [1] * 15)
header[0].markdown("**#**")

for c in range(15):
    header[c + 1].markdown(f"**{chr(65 + c)}**")

# Board: 15 rows x 15 buttons
for r in range(15):
    cols = st.columns([0.55] + [1] * 15)
    cols[0].markdown(f"**{r + 1}**")

    for c in range(15):
        cols[c + 1].button(
            "⭐" if (r, c) == (7, 7) else "·",
            key=f"test_{r}_{c}",
            on_click=select_square,
            args=(r, c)
        )

if st.session_state.selected is not None:
    r, c = st.session_state.selected
    st.success(f"Selected square: {chr(65 + c)}{r + 1}")