import streamlit as st
import numpy as np

st.set_page_config(page_title="🎬 Movie Elimination", layout="centered")

st.title("🎬 Movie Elimination Game")
st.markdown("At each step, one movie is randomly removed after shuffling. Only one winner will remain!")

# --- Session state storage ---
if "movies" not in st.session_state:
    st.session_state.movies = []
if "step" not in st.session_state:
    st.session_state.step = 0
if "winner" not in st.session_state:
    st.session_state.winner = None

# --- Initial movie input ---
if not st.session_state.movies and not st.session_state.winner:
    st.subheader("📥 Enter a list of movies (one per line):")
    user_input = st.text_area("Movies", height=200, placeholder="movie1\nmovie2\nmovie3")
    if st.button("Start Elimination"):
        films = [f.strip() for f in user_input.strip().splitlines() if f.strip()]
        if len(films) < 2:
            st.error("Please enter at least two movies.")
        else:
            st.session_state.movies = films
            st.session_state.step = 1
            st.experimental_rerun()

# --- Elimination process ---
elif st.session_state.movies and not st.session_state.winner:
    st.subheader(f"🎬 Step {st.session_state.step}")
    st.write("🔄 Shuffling and eliminating one movie at random...")

    # Shuffle and remove one
    shuffled = list(np.random.permutation(st.session_state.movies))
    idx = np.random.randint(len(shuffled))
    removed = shuffled.pop(idx)

    st.markdown("**🎲 New movie order:**")
    st.write(shuffled + [removed])

    st.markdown(f"**❌ Eliminated:** `{removed}`")

    # Update state
    st.session_state.movies = shuffled
    st.session_state.step += 1

    if len(shuffled) == 1:
        st.session_state.winner = shuffled[0]
    else:
        st.button("➡️ Next Step", on_click=lambda: st.experimental_rerun())

# --- Final winner display ---
if st.session_state.winner:
    st.subheader("🏆 Winner:")
    st.success(f"🎥 {st.session_state.winner}")

    if st.button("🔁 Restart"):
        st.session_state.movies = []
        st.session_state.step = 0
        st.session_state.winner = None
        st.experimental_rerun()
