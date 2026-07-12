import os
import tempfile

import streamlit as st

from main import run_pipeline
from core.rag_engine import ask_question


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Video Researcher",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 20% 0%, #172033 0%, transparent 30%),
                radial-gradient(circle at 100% 20%, #18152f 0%, transparent 25%),
                #090b10;
        }

        [data-testid="stSidebar"] {
            background: #0d1017;
            border-right: 1px solid #222733;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

        .hero {
            padding: 1rem 0 2rem 0;
        }

        .hero-title {
            font-size: 3.4rem;
            font-weight: 750;
            letter-spacing: -0.06em;
            margin-bottom: 0;
            background: linear-gradient(
                90deg,
                #ffffff 0%,
                #c5c9d3 50%,
                #7c83ff 100%
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            color: #8d94a5;
            font-size: 1.05rem;
            max-width: 650px;
            margin-top: 0.7rem;
        }

        .section-label {
            color: #7c83ff;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            margin-bottom: 0.4rem;
        }

        .result-card {
            background: rgba(18, 21, 30, 0.85);
            border: 1px solid #252a38;
            border-radius: 18px;
            padding: 1.4rem;
            margin-bottom: 1rem;
        }

        .result-card h3 {
            margin-top: 0;
            font-size: 1.05rem;
        }

        .status-ready {
            color: #4ade80;
            font-size: 0.85rem;
        }

        .status-idle {
            color: #8d94a5;
            font-size: 0.85rem;
        }

        div[data-testid="stButton"] > button {
            border-radius: 10px;
            font-weight: 600;
            min-height: 44px;
        }

        div[data-testid="stChatMessage"] {
            background: rgba(18, 21, 30, 0.65);
            border: 1px solid #252a38;
            border-radius: 14px;
            padding: 0.4rem;
        }

        hr {
            border-color: #222733;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

defaults = {
    "result": None,
    "messages": [],
    "processing": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("## ◉ VidMind")
    st.caption("AI Video Intelligence")

    st.divider()

    st.markdown("### Input source")

    input_type = st.radio(
        "Source type",
        ["YouTube URL", "Upload video"],
        label_visibility="collapsed",
    )

    source = None
    uploaded_file = None

    if input_type == "YouTube URL":
        source = st.text_input(
            "Video URL",
            placeholder="https://youtube.com/watch?v=...",
        )

    else:
        uploaded_file = st.file_uploader(
            "Upload video",
            type=["mp4", "mov", "mkv", "avi", "webm"],
        )

    language = st.selectbox(
        "Language",
        ["english", "hinglish"],
        format_func=lambda value: value.title(),
    )

    st.divider()

    process_button = st.button(
        "Analyze video",
        type="primary",
        use_container_width=True,
    )

    if st.session_state.result:
        st.markdown(
            '<p class="status-ready">● Analysis ready</p>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<p class="status-idle">● Waiting for video</p>',
            unsafe_allow_html=True,
        )

    st.divider()

    if st.button("Clear session", use_container_width=True):
        st.session_state.result = None
        st.session_state.messages = []
        st.rerun()

    st.caption("Transcription · Insights · RAG")


# ---------------------------------------------------------
# PROCESS VIDEO
# ---------------------------------------------------------

if process_button:
    pipeline_source = source
    temporary_path = None

    if input_type == "Upload video":
        if uploaded_file is None:
            st.sidebar.error("Upload a video first.")
            st.stop()

        suffix = os.path.splitext(uploaded_file.name)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temporary_path = temp_file.name

        pipeline_source = temporary_path

    elif not source or not source.strip():
        st.sidebar.error("Enter a YouTube URL.")
        st.stop()

    try:
        st.session_state.processing = True

        with st.status(
            "Analyzing video...",
            expanded=True,
        ) as status:
            st.write("Extracting audio")
            st.write("Transcribing content")
            st.write("Generating AI insights")
            st.write("Building knowledge index")

            result = run_pipeline(
                pipeline_source,
                language,
            )

            st.session_state.result = result
            st.session_state.messages = []

            status.update(
                label="Analysis complete",
                state="complete",
                expanded=False,
            )

    except Exception as error:
        st.error(f"Pipeline failed: {error}")

    finally:
        st.session_state.processing = False

        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="section-label">Video Intelligence Workspace</div>
        <div class="hero-title">Understand any video.</div>
        <div class="hero-subtitle">
            Transcribe meetings and videos, extract decisions and action
            items, then ask questions directly against the content.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# EMPTY STATE
# ---------------------------------------------------------

if not st.session_state.result:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="result-card">
                <h3>01 · Transcribe</h3>
                <p>
                    Convert long-form video and audio into searchable text.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="result-card">
                <h3>02 · Extract insights</h3>
                <p>
                    Surface summaries, decisions, questions and action items.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="result-card">
                <h3>03 · Ask anything</h3>
                <p>
                    Chat with the video through your existing RAG pipeline.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.info("Add a YouTube URL or upload a video from the sidebar.")

    st.stop()


# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------

result = st.session_state.result

st.markdown(
    '<div class="section-label">Current analysis</div>',
    unsafe_allow_html=True,
)

st.title(result["title"])

overview_tab, transcript_tab, chat_tab = st.tabs(
    [
        "Overview",
        "Transcript",
        "Ask AI",
    ]
)


# ---------------------------------------------------------
# OVERVIEW TAB
# ---------------------------------------------------------

with overview_tab:
    st.markdown("### Executive summary")

    st.markdown(
        f"""
        <div class="result-card">
            {result["summary"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:
        st.markdown("### Action items")

        with st.container(border=True):
            st.markdown(result["action_items"])

        st.markdown("### Open questions")

        with st.container(border=True):
            st.markdown(result["open_questions"])

    with right:
        st.markdown("### Key decisions")

        with st.container(border=True):
            st.markdown(result["key_decisions"])


# ---------------------------------------------------------
# TRANSCRIPT TAB
# ---------------------------------------------------------

with transcript_tab:
    transcript = result["transcript"]

    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown("### Full transcript")

    with col2:
        st.download_button(
            "Download transcript",
            data=transcript,
            file_name="transcript.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.text_area(
        "Transcript",
        value=transcript,
        height=600,
        label_visibility="collapsed",
    )


# ---------------------------------------------------------
# CHAT TAB
# ---------------------------------------------------------

with chat_tab:
    st.markdown("### Ask your video")
    st.caption(
        "Answers are generated from the analyzed transcript."
    )

    if not st.session_state.messages:
        st.markdown(
            """
            Try asking:

            - What are the main topics?
            - What decisions were made?
            - What should I do next?
            - Explain the most important point.
            """
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask a question about this video..."
    )

    if question:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching video context..."):
                try:
                    answer = ask_question(
                        result["rag_chain"],
                        question,
                    )

                    st.markdown(answer)

                except Exception as error:
                    answer = (
                        f"Unable to answer the question: {error}"
                    )

                    st.error(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )