# AI Video Assistant

An AI-powered video and audio analysis application built with Streamlit, Whisper, LangChain, Mistral AI, and ChromaDB.

The application processes video or audio content, generates transcripts and summaries, extracts structured insights, and provides a Retrieval-Augmented Generation (RAG) based question-answering interface.

## Features

- Process video and audio content
- Download and extract audio from supported URLs
- Speech-to-text transcription using OpenAI Whisper
- AI-generated meeting and video summaries
- Automatic title generation
- Extract action items
- Extract key decisions
- Extract important questions
- Semantic document chunking
- Vector storage using ChromaDB
- RAG-based question answering
- Interactive Streamlit interface

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| Streamlit | Web interface |
| OpenAI Whisper | Speech-to-text transcription |
| LangChain | LLM and RAG orchestration |
| Mistral AI | Language model |
| ChromaDB | Vector database |
| Sentence Transformers | Text embeddings |
| yt-dlp | Video and audio acquisition |
| pydub | Audio processing |
| FFmpeg | Media processing |

## Project Structure

```text
ai-video-assistant/
│
├── core/
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarizer.py
│   ├── transcriber.py
│   └── vector_store.py
│
├── utils/
│   └── audio_processor.py
│
├── .streamlit/
│   └── config.toml
│
├── main.py
├── streamlit_app.py
├── test.py
├── requirements.txt
├── packages.txt
├── .gitignore
└── README.md
```

## Application Pipeline

The application follows the pipeline below:

```text
Video / Audio Input
        |
        v
Audio Processing
        |
        v
Whisper Transcription
        |
        v
Transcript Processing
        |
        +----------------------+
        |                      |
        v                      v
AI Summarization        Insight Extraction
                               |
                     +---------+---------+
                     |         |         |
                     v         v         v
                Action Items Decisions Questions
        |
        v
Text Chunking
        |
        v
Sentence Transformer Embeddings
        |
        v
ChromaDB Vector Store
        |
        v
RAG Question Answering
        |
        v
Streamlit Interface
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-video-assistant.git
cd ai-video-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment.

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

FFmpeg is required for audio and video processing.

Verify the installation:

```bash
ffmpeg -version
```

## Environment Variables

Create a `.env` file in the project root.

```env
MISTRAL_API_KEY=your_mistral_api_key
```

Do not commit the `.env` file to GitHub.

## Running the Application

Run the Streamlit application:

```bash
streamlit run streamlit_app.py
```

The application will open in your browser.

The default local address is usually:

```text
http://localhost:8501
```

## Core Modules

### `audio_processor.py`

Handles video and audio acquisition and audio preprocessing using `yt-dlp` and `pydub`.

### `transcriber.py`

Performs speech-to-text transcription using OpenAI Whisper.

### `summarizer.py`

Generates summaries and titles using Mistral AI and LangChain.

### `extractor.py`

Extracts structured information from transcripts, including:

- Action items
- Key decisions
- Questions

### `vector_store.py`

Splits transcript content, generates embeddings, and stores vectors in ChromaDB.

### `rag_engine.py`

Builds the Retrieval-Augmented Generation pipeline and answers questions using relevant transcript context.

## Deployment

The application is designed for deployment using Streamlit Community Cloud.

Deployment files:

```text
requirements.txt
packages.txt
streamlit_app.py
```

`requirements.txt` contains Python dependencies.

`packages.txt` installs the FFmpeg system dependency required for media processing.

Environment secrets should be configured using Streamlit Community Cloud secrets instead of committing a `.env` file.

## Security

The following files and directories are excluded from Git:

```text
.env
.venv/
downloads/
vector_db/
.streamlit/secrets.toml
```

API keys and other credentials should never be committed to the repository.

## Future Improvements

- Support additional video platforms
- Improve transcription performance
- Add speaker diarization
- Add multilingual transcription
- Add transcript export
- Add PDF report generation
- Add persistent cloud vector storage
- Add user authentication
- Improve RAG retrieval quality

## License

This project is currently provided without a license.

## Author

Developed by Mohit Singhal.