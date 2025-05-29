# Intelligent Advisor - RAG Chatbot

This project is a RAG (Retrieval Augmented Generation) based chatbot designed to answer questions about Taiwanese labor regulations. It uses a Django backend, a simple HTML/CSS/JavaScript frontend, ChromaDB for vector storage, and OpenAI's API for text embeddings and language model generation.

## Features

*   **Conversational Interface**: Chat with an AI to get answers about labor laws.
*   **Retrieval Augmented Generation (RAG)**: The chatbot retrieves relevant sections from "Labor_regulations.pdf" to provide context-aware answers.
*   **PDF Document Ingestion**: Automatically processes and chunks a PDF document to build its knowledge base.
*   **Vector Search**: Uses ChromaDB and OpenAI embeddings to find the most relevant document chunks for a given query.
*   **Dark Theme UI**: A clean, dark-themed user interface for comfortable interaction.

## Tech Stack

*   **Backend**: Python, Django
*   **Frontend**: HTML, CSS, JavaScript
*   **Vector Database**: ChromaDB
*   **LLM & Embeddings**: OpenAI API (GPT models, text-embedding-3-small)
*   **PDF Processing**: PyPDF2

## Prerequisites (macOS)

*   **macOS**: This guide assumes you are on a macOS system.
*   **Python 3.8+**: Ensure Python 3.8 or a newer version is installed. You can check with `python3 --version`.
*   **Git**: For cloning the repository.
*   **A Conda environment or Python virtual environment (venv)**: Recommended for managing project dependencies. This guide will use `venv` as an example.

## Setup and Installation (macOS)

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd gpt_rag_demo
    ```

2.  **Create and Activate a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(If you are using Conda, you would use `conda create -n your_env_name python=3.x` and `conda activate your_env_name`)*

3.  **Install Dependencies:**
    Make sure you have a `requirements.txt` file in your project root. If not, generate it from your working environment.
    ```bash
    pip install -r requirements.txt
    ```
    *(Common dependencies for this project would include `django`, `openai`, `chromadb`, `pypdf2`)*

4.  **Set Up Environment Variables:**
    This project requires an OpenAI API Key and a Django Secret Key. These should **NEVER** be hardcoded into your source code or committed to Git. We will store them as environment variables in your `~/.zshrc` file (if you use Zsh, the default shell on modern macOS).

    *   **a. Obtain an OpenAI API Key:**
        1.  Go to the OpenAI API platform.
        2.  Sign up or log in to your account.
        3.  Navigate to the API keys section (usually under your account settings or "API Keys").
        4.  Create a new secret key. **Copy this key immediately and store it securely.** You won't be able to see it again.

    *   **b. Generate a Django `SECRET_KEY`:**
        You can generate a strong secret key using Python. Open a Python interpreter:
        ```bash
        python3
        ```
        Then run the following commands:
        ```python
        python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
        ```
        This will output a random string. Copy this string. For example: `'your_generated_django_secret_key_here'` (use the actual output).

    *   **c. Add Keys to `~/.zshrc`:**
        Open your Zsh configuration file using a text editor like `nano` or `vim`:
        ```bash
        nano ~/.zshrc
        ```
        Add the following lines to the end of the file, replacing the placeholder values with your actual keys:
        ```bash
        export OPENAI_API_KEY="sk-your_openai_api_key_here"
        export DJANGO_SECRET_KEY="your_generated_django_secret_key_here"
        ```
        Save the file (Ctrl+O, then Enter in `nano`, then Ctrl+X to exit).
        Apply the changes to your current terminal session:
        ```bash
        source ~/.zshrc
        ```
        Your Django application (`settings.py`) and `chroma_rag.py` will now be able to access these keys via `os.getenv()`.

5.  **Prepare PDF Data and Build Vector Database:**
    *   Place your PDF document named `Labor_regulations.pdf` in the project's root directory (e.g., `/Users/oneil/Documents/AI_agent/gpt_rag_demo/Labor_regulations.pdf`).
    *   **Important:** Before running the Django server for the first time, you need to manually run the `chroma_rag.py` script to process the PDF, create embeddings, and build the initial vector database. Execute the following command from your project's root directory (where `manage.py` is located), ensuring your virtual environment is active and `OPENAI_API_KEY` is set:
        ```bash
        python chatbot/chroma_rag.py
        ```
        This script will create a `chroma_store` directory and populate it. Subsequent runs of the Django application will load the existing database.

6.  **Run Django Migrations (Standard Practice):**
    Although this specific project might not have custom database models requiring extensive migrations beyond Django's defaults, it's good practice.
    ```bash
    python manage.py migrate
    ```

7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
    The application should now be running, typically at `http://127.0.0.1:8000/`.

## Usage

1.  Open your web browser and navigate to `http://127.0.0.1:8000/`.
2.  You will see the chat interface titled "智能幕僚".
3.  Type your question about Taiwanese labor regulations into the input box at the bottom.
4.  Press Enter or click the "Send" button.
5.  The AI will process your question, retrieve relevant information from the PDF, and provide an answer.

## Important Security Note

*   **NEVER commit your `API_key.py` file (if you still have it) or hardcode your `OPENAI_API_KEY` or `DJANGO_SECRET_KEY` directly into your source code.**
*   Ensure that `API_key.py`, `.env` files (if you choose to use them for local development), `chroma_store/`, and `db.sqlite3` are listed in your `.gitignore` file.
*   Always use environment variables for sensitive keys, as described in the setup instructions.
