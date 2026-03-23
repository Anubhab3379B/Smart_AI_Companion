# Smart AI Companion

A modular, privacy-focused AI companion for science, math, and exam preparation.

## Features
- **Project Structure**: Modular Python package `smart_companion`.
- **Core Inference**: Supports local GGUF models via `llama-cpp-python`.
- **RAG Memory**: ChromaDB + LangChain for persistent memory.
- **Tools**: Math (SymPy), Code Execution (PythonREPL), Web Search.
- **Voice**: Local TTS and STT capabilities.
- **Exam Prep**: Curriculum management and Tutor Mode.
- **UI**: Modern Streamlit interface.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Download a model (optional, or bring your own GGUF):
   ```bash
   python scripts/download_model.py
   ```

3. Run the UI:
   ```bash
   streamlit run smart_companion/interfaces/web_ui.py
   ```

## Usage
- **Chat**: Open the UI and start chatting.
- **Tutor Mode**: Select 'Tutor Mode' in the sidebar to focus on a specific subject.
- **Recorder**: Use 'Class Recorder' to record and summarize lectures.
