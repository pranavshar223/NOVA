# NOVA - Desktop Assistant

## Next-Gen Operational Virtual Assistant

NOVA is an advanced AI Assistant that not only provides intelligent text responses but also performs real-world system tasks based on user commands. It can adjust volume and brightness, open applications, send WhatsApp messages, and send emails — offering a seamless virtual assistant experience.

---

## DEMO

*Demo pics are added here.*

---

## FEATURES

- AI-powered chatbot responses
- Control system volume (increase/decrease)
- Adjust laptop brightness (increase/decrease)
- Open applications on user demand
- Send WhatsApp messages
- Send emails

---

## INSTALLATION

### Clone the repository:

```bash
git clone https://github.com/pranavshar223/NOVA.git
```

### Navigate into the project directory:

```bash
cd NOVA
```

### Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Run the application:

```bash
python frontend.py
```

## Usage

- Run `frontend.py` to start NOVA.
- Give voice or text commands like:
  - "Increase the volume"
  - "Decrease the brightness"
  - "Open Chrome"
  - "Send WhatsApp message to John"
  - "Send an email to my manager"

---

# Quick Setup

## 1. Clone the repository

```bash
git clone https://github.com/pranavshar223/NOVA.git
cd NOVA
```

## 2. Create virtual environment

```bash
python -m venv myenv
```

## 3. Activate virtual environment

**On Windows PowerShell:**
```bash
.\myenv\Scripts\Activate.ps1
```

**On Windows CMD:**
```bash
myenv\Scripts\activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Create a .env file

Create a file named `.env` in the project root and add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3-flash-preview

FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True
BACKEND_URL=http://127.0.0.1:5000/chat
```

## 6. Run the backend

```bash
python backend/app.py
```

## 7. Run the frontend

Open a second terminal and run:

```bash
python frontend/main.py
```

---

# How It Works

1. The user enters a message in the PyQt frontend
2. The frontend sends the message to the Flask backend
3. The backend processes the request using:
   - Assistant logic
   - Gemini AI
   - System task handlers
4. The backend returns a response
5. The frontend displays the response in the chat UI

---

# Example Commands

- `hi`
- `what is python`
- `search wikipedia about artificial intelligence`
- `play believer on youtube`
- `set brightness to 50`
- `set volume to 30`

> **Be careful with commands like shutdown, restart, and sleep while testing.**

---

# Future Goals

The following improvements are planned for future versions of NOVA Assistant:

## UI/UX Improvements

- Typing indicator animation
- Assistant avatar/logo
- Settings panel
- Better chat bubble styling
- Keyboard shortcuts
- Header actions like clear chat or menu button

## Assistant Features

- Voice input with microphone button
- Text-to-speech toggle
- Auto-start Flask backend from PyQt
- More desktop automation commands
- Open installed applications
- Browser search support

## Data and Persistence

- Chat history saving
- SQLite database integration
- User preferences/settings storage
- Session-based conversation history

## Deployment

- Build as .exe
- Custom application icon
- Single-click launcher
- Better packaging for backend + frontend

---

# Current Status

This project is currently in an active improvement stage. The main architecture is working and includes:

- Working frontend and backend
- Working Gemini integration
- Working system controls
- Modern chat UI
- Threading support
- Clean code structure

---

# Important Notes

- This app is designed to run locally on your machine.
- The Flask backend runs on `127.0.0.1:5000`, which means it is a local server, not a public website.
- Some features require internet access, such as:
  - Gemini AI
  - Wikipedia
  - YouTube
- Some features work locally without internet, such as:
  - Brightness control
  - Volume control
  - Shutdown/restart/sleep

---

# Security Note

Do not upload your `.env` file or API keys to GitHub.

Make sure your `.gitignore` includes:

```gitignore
.env
myenv/
__pycache__/
.idea/
```

If you accidentally uploaded your API key before, regenerate it immediately.

---

# Author

Pranav Sharma
