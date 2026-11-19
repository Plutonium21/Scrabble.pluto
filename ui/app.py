import streamlit as st
from engine.game_state import GameState
from engine.dictionary import load_dictionary
from engine.rules import validate_move,apply_move
from ai.trie import Trie
from ai.evaluator import choose_move
from engine.board import premium_at

st.set_page_config(page_title="Scrabble.pluto",page_icon="🔠",layout="wide")

@st.cache_resource
def load_assets():
    dictionary,path = load_dictionary()
    return dictionary,Trie(dictionary),path

dictionary,trie,lexicon_source = load_assets()

if "game" not in st.session_state:
    st.session_state.game = GameState()
if "selected_square" not in st.session_state:
    st.session_state.selected_square = None
if "show_placement" not in st.session_state:
    st.session_state.show_placement = False

game = st.session_state.game

# ==================================================
# AI TURN EXECUTION
# ==================================================

if game.turn == "AI" and not game.game_over:

    with st.status(
        "🤖 AI's Turn — Thinking...",
        expanded=True
    ) as ai_status:

        # Ask the AI to find its best legal move.
        ai_move = choose_move(
            game.board,
            game.racks["AI"],
            dictionary,
            trie
        )

        if ai_move is not None:

            # Apply the selected move to the board.
            apply_move(
                game.board,
                game.racks["AI"],
                ai_move
            )

            # Update AI score, history, rack and turn.
            game.finish_turn("AI", ai_move)

            ai_status.update(
                label=f"🤖 AI played {ai_move['word']}! Your Turn.",
                state="complete",
                expanded=False
            )

        else:

            # No legal move available: AI passes.
            game.finish_turn("AI")

            ai_status.update(
                label="🤖 AI passed. Your Turn!",
                state="complete",
                expanded=False
            )

    # Clear any leftover human placement state.
    st.session_state.selected_square = None
    st.session_state.pending_move = None
    st.session_state.show_placement = False

# ==================================================
# BOARD INTERACTION
# ==================================================

def select_square(r, c):
    """Handle selection of a board square."""

    # Only allow the human player to interact with the board.
    if game.turn != "You" or game.game_over:
        return

    st.session_state.selected_square = (r, c)
    st.session_state.pending_move = None
    st.session_state.show_placement = True


# ==================================================
# POPUP: WORD PLACEMENT
# ==================================================

@st.dialog("Place your word")
def placement_dialog():

    if st.session_state.selected_square is None:
        st.info("Select a board square first.")
        return

    r, c = st.session_state.selected_square

    st.write(
        f"Starting square: **{chr(65+c)}{r+1}**"
    )

    with st.form("place_word_form"):

        word = st.text_input(
            "Your word",
            max_chars=15,
            placeholder="e.g. PLANET"
        ).upper().strip()

        direction = st.radio(
            "Direction",
            ["H", "V"],
            horizontal=True,
            format_func=lambda x: (
                "Horizontal →" if x == "H"
                else "Vertical ↓"
            )
        )

        preview = st.form_submit_button("Check move")

    if preview:

        ok, message, move = validate_move(
            game.board,
            game.racks["You"],
            word,
            r,
            c,
            direction,
            dictionary
        )

        if ok:
            st.success(
                f"Legal move · {move['score']} points"
            )
            st.session_state.pending_move = move

        else:
            st.error(message)
            st.session_state.pending_move = None

    pending = st.session_state.get("pending_move")

    if pending and pending["row"] == r and pending["col"] == c:

        st.write(
            "**Preview:** " +
            " · ".join(
                f"{chr(65+cc)}{rr+1}: {tile.letter}"
                for (rr, cc), tile
                in pending["placements"].items()
            )
        )

        if st.button(
            "Play this word",
            type="primary",
            use_container_width=True
        ):

            apply_move(
                game.board,
                game.racks["You"],
                pending
            )

            game.finish_turn("You", pending)

            st.session_state.pending_move = None
            st.session_state.show_placement = False
            st.session_state.selected_square = None

            st.rerun()


# ==================================================
# POPUP: MOVE HISTORY
# ==================================================

@st.dialog("Move History", width="large")
def move_history_dialog():

    st.subheader("Previous moves")

    if not game.history:
        st.info("No moves have been played yet.")

    else:
        for index, item in enumerate(reversed(game.history)):
            st.write(f"**{index + 1}.** {item}")


# ==================================================
# POPUP: HOW TO PLAY
# ==================================================

@st.dialog("How to Play Scrabble", width="large")
def instructions_dialog():

    st.subheader("Basic rules")

    st.markdown("""
    1. Each player starts with seven tiles.
    2. Your first word must cover the centre star.
    3. Every subsequent word must connect to an existing tile.
    4. Words can be placed horizontally or vertically.
    5. All newly formed words must be valid dictionary words.
    6. Double and triple letter/word squares increase your score.
    7. Using all seven rack tiles earns a 50-point bonus.

    ### Special tiles

    - **3W:** Triple Word Score
    - **2W:** Double Word Score
    - **3L:** Triple Letter Score
    - **2L:** Double Letter Score
    - **?:** Blank tile, worth zero points

    ### Winning

    The game ends according to the end-game rules.
    The player with the highest final score wins.
    """)


st.markdown("""
<style>
/* Overall page */
.block-container {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    max-width: 1600px;
}

/* Headings */
h1 {
    margin-bottom: 0.15rem;
}

h2, h3 {
    margin-top: 0.25rem;
    margin-bottom: 0.4rem;
}

/* Square board, constrained by screen height */
.st-key-scrabble_board {
    width: min(100%, 68vh);
    margin-left: auto;
    margin-right: auto;
}

/* Remove vertical spacing between board rows */
.st-key-scrabble_board [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

/* Square interactive cells */
.st-key-scrabble_board [data-testid="stButton"] button {
    width: 100%;
    aspect-ratio: 1 / 1;
    height: auto;
    min-height: 0;
    padding: 0 !important;
    border-radius: 3px;
    font-size: clamp(8px, 0.75vw, 12px);
    font-weight: 800;
    line-height: 1;
}

/* Board coordinates */
.st-key-scrabble_board [data-testid="stMarkdownContainer"] p {
    font-size: 9px;
    font-weight: 700;
    text-align: center;
    margin: 0;
    padding: 0;
}

/* Rack tiles */
.tile-rack {
    background: #e7c58c;
    color: #352817;
    border: 1px solid #b48a50;
    border-radius: 8px;
    padding: 9px 3px;
    text-align: center;
    font-size: 20px;
    font-weight: 900;
}

.tile-rack small {
    display: block;
    font-size: 9px;
    font-weight: 600;
}

/* Compact sidebar controls */
.st-key-side_actions button {
    min-height: 38px;
}


/* Aggressively compact the board's vertical layout */
.st-key-scrabble_board [data-testid="stVerticalBlock"] {
    gap: 0px !important;
    row-gap: 0px !important;
}

/* Remove spacing between individual board elements */
.st-key-scrabble_board [data-testid="stElementContainer"] {
    margin: 0 !important;
    padding: 0 !important;
    min-height: 0 !important;
}

/* Remove button wrapper spacing */
.st-key-scrabble_board [data-testid="stButton"] {
    margin: 0 !important;
    padding: 0 !important;
}

/* Keep cells compact */
.st-key-scrabble_board [data-testid="stButton"] button {
    margin: 0 !important;
    padding: 0 !important;
    border-radius: 2px !important;
}


</style>
""", unsafe_allow_html=True)


# ==================================================
# MAIN HEADER
# ==================================================

st.title("Scrabble.pluto")
st.caption("Build words, score big, and challenge the computer.")

if lexicon_source == "data\\words.txt":
    lexicon_source = "Collins Scrabble Words (2019)"

st.info(
    f"Lexicon: **{lexicon_source}** · "
    f"{len(dictionary):,} words loaded"
)


# ==================================================
# MAIN GAME LAYOUT
# ==================================================

board_column, side_column = st.columns(
    [3.2, 1.2],
    gap="large"
)


# ==================================================
# LEFT COLUMN: BOARD
# ==================================================

with board_column:

    st.subheader("The Board")
    st.caption("Select a square to place your word.")

    with st.container(key="scrabble_board"):

        # Column headings
        header = st.columns(
            [0.35] + [1] * 15,
            gap=None
        )

        header[0].markdown("**#**")

        for c in range(15):
            header[c + 1].markdown(
                f"**{chr(65 + c)}**"
            )

        # Collect styles for occupied tiles
        occupied_tile_rules = []

        # Board rows
        for r in range(15):

            cols = st.columns(
                [0.35] + [1] * 15,
                gap=None
            )

            cols[0].markdown(f"**{r + 1}**")

            for c in range(15):

                tile = game.board[r][c]

                if tile is not None:

                    label = (
                        tile.letter.lower()
                        if tile.is_blank
                        else tile.letter
                    )
                    occupied_tile_rules.append(f"""
                        .st-key-sq_{r}_{c} button {{
                            background-color: #FFD54F !important;
                            color: #352817 !important;
                            border: 1px solid #B8860B !important;
                        }}

                        .st-key-sq_{r}_{c} button p {{
                            color: #352817 !important;
                        }}
                    """)
                else:

                    premium = premium_at(r, c)

                    label = {
                        "TW": "3W",
                        "DW": "2W",
                        "TL": "3L",
                        "DL": "2L",
                        "": "·"
                    }[premium]

                    if (r, c) == (7, 7):
                        label = "★"

                cols[c + 1].button(
                    label,
                    key=f"sq_{r}_{c}",
                    help=f"{chr(65+c)}{r+1}",
                    on_click=select_square,
                    args=(r, c),
                    use_container_width=True
                )
        # NEW: inject CSS after rendering all cells
        st.markdown(
            "<style>" + "\n".join(occupied_tile_rules) + "</style>",
            unsafe_allow_html=True
        )

# ==================================================
# RIGHT COLUMN: GAME CONTROLS
# ==================================================

with side_column:

    # ----------------------------------------------
    # SCORE
    # ----------------------------------------------

    st.subheader("Score")

    score1, score2 = st.columns(2)

    score1.metric(
        "You",
        game.scores["You"]
    )

    score2.metric(
        "Computer",
        game.scores["AI"]
    )

    st.divider()

    # ----------------------------------------------
    # RACK
    # ----------------------------------------------

    st.subheader("Your Rack")

    rack = game.racks["You"]

    rack_cols = st.columns(4, gap="small")

    for i, tile in enumerate(rack):

        with rack_cols[i % 4]:

            st.markdown(
                f"""
                <div class="tile-rack">
                    {tile.letter}
                    <small>{tile.value} pts</small>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    # ----------------------------------------------
    # TURN INFORMATION
    # ----------------------------------------------

    st.subheader("Your Turn")
    if game.game_over:
        st.error("🏁 Game Over!")

    elif game.turn == "You":
        st.success("🟢 Your Turn")

    else:
        st.info("🤖 AI's Turn — Thinking...")

    st.write(
        f"Tiles in bag: **{len(game.bag.tiles)}**"
    )

    if st.session_state.selected_square is not None:

        r, c = st.session_state.selected_square

        st.success(
            f"Selected: {chr(65+c)}{r+1}"
        )

    # ----------------------------------------------
    # ACTION BUTTONS
    # ----------------------------------------------

    with st.container(key="side_actions"):

        if not game.game_over and game.turn == "You":

            if st.button(
                "Pass Turn",
                use_container_width=True
            ):

                game.finish_turn("You")

                st.session_state.selected_square = None
                st.session_state.pending_move = None
                st.session_state.show_placement = False

                st.rerun()

        if st.button(
            "New Game",
            use_container_width=True
        ):

            st.session_state.game = GameState()
            st.session_state.selected_square = None
            st.session_state.pending_move = None
            st.session_state.show_placement = False
            st.rerun()

    st.divider()

    # ----------------------------------------------
    # INFORMATION POPUPS
    # ----------------------------------------------

    st.subheader("More")

    if st.button(
        "📜 Move History",
        use_container_width=True
    ):
        move_history_dialog()

    if st.button(
        "📖 How to Play",
        use_container_width=True
    ):
        instructions_dialog()


# ==================================================
# PLACEMENT POPUP
# ==================================================

if st.session_state.show_placement:
    placement_dialog()


# ==================================================
# GAME STATUS
# ==================================================

if game.game_over:

    st.success("Game over!")

    if game.scores["You"] > game.scores["AI"]:
        st.balloons()
        st.write("You won!")

    elif game.scores["You"] < game.scores["AI"]:
        st.write("The computer won.")

    else:
        st.write("It's a draw.")
