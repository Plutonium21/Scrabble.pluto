
import streamlit as st

from engine.game_state import GameState
from engine.dictionary import load_dictionary
from engine.board import premium_at


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Scrabble Club1",
    page_icon="🔠",
    layout="wide"
)


# --------------------------------------------------
# LOAD GAME ASSETS
# --------------------------------------------------

@st.cache_resource
def load_lexicon():
    return load_dictionary()


dictionary, lexicon_source = load_lexicon()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "game" not in st.session_state:
    st.session_state.game = GameState()

if "selected_square" not in st.session_state:
    st.session_state.selected_square = None


game = st.session_state.game


def select_square(r, c):
    st.session_state.selected_square = (r, c)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🔠 Scrabble Club — Diagnostic")

st.info(
    f"Lexicon: {lexicon_source} | "
    f"{len(dictionary):,} words loaded"
)

score1, score2 = st.columns(2)

score1.metric("Your score", game.scores["You"])
score2.metric("Computer score", game.scores["AI"])


# --------------------------------------------------
# BOARD
# --------------------------------------------------

st.subheader("Scrabble Board")

header = st.columns([0.55] + [1] * 15)

header[0].markdown("**#**")

for c in range(15):
    header[c + 1].markdown(f"**{chr(65 + c)}**")


for r in range(15):

    cols = st.columns([0.55] + [1] * 15)

    cols[0].markdown(f"**{r + 1}**")

    for c in range(15):

        tile = game.board[r][c]

        if tile is not None:
            label = tile.letter
        elif (r, c) == (7, 7):
            label = "⭐"
        else:
            premium = premium_at(r, c)

            label = {
                "TW": "3W",
                "DW": "2W",
                "TL": "3L",
                "DL": "2L",
                "": "·"
            }[premium]

        cols[c + 1].button(
            label,
            key=f"test_sq_{r}_{c}",
            on_click=select_square,
            args=(r, c),
            use_container_width=True
        )


# --------------------------------------------------
# CLICK RESULT
# --------------------------------------------------

if st.session_state.selected_square is not None:

    r, c = st.session_state.selected_square

    st.success(
        f"Selected square: {chr(65 + c)}{r + 1}"
    )


# --------------------------------------------------
# RACK
# --------------------------------------------------

st.divider()
st.subheader("Your rack")

rack_cols = st.columns(7)

for i, tile in enumerate(game.racks["You"]):

    rack_cols[i].markdown(
        f"### {tile.letter}\n{tile.value} points"
    )


st.caption("Diagnostic mode: word placement and AI are temporarily disabled.")
