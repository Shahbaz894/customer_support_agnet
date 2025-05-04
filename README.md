#     $ conda activate E:\customer_support_agnet\venv
#
# To deactivate an active environment, use
#
#     $ conda deactivate



📄 README.md
markdown
Copy
Edit
# 🤖 Customer Support Agent

This is a simple AI-powered **Customer Support Agent** web application built using **FastAPI**. It uses product review data from Amazon to simulate a chatbot that can answer customer queries about products intelligently.

---

## 🚀 Features

- Conversational interface like a chatbot
- Uses Amazon product review data for product context
- Real-time message exchange using AJAX
- Responsive and modern frontend (Bootstrap, jQuery)
- Backend powered by FastAPI and Jinja2 templates

---

## 🏗️ Project Structure

customer_support_agent/
│
├── main.py # FastAPI backend entry point
├── templates/
│ └── index.html # Chat UI
├── static/
│ └── style.css # Custom styles
├── requirements.txt # Python dependencies
└── README.md # You're reading it!

yaml
Copy
Edit

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Shahbaz894/customer_support_agnet.git
cd customer_support_agnet
2. Create and Activate Virtual Environment

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
3. Install Dependencies

pip install -r requirements.txt
If you encounter jinja2 must be installed error:


pip install jinja2
🚦 Running the App
Use this command to start the FastAPI server:


uvicorn main:app --reload
Open your browser and visit: http://127.0.0.1:8000

🧠 How It Works
User Interface:

Built using HTML, Bootstrap 4, and jQuery

Chat-like UI with message bubbles and user avatars

Backend:

FastAPI receives user input via AJAX POST

A simple NLP logic (or mock response) generates a response

Returns it back to frontend for display

Data Source:

Amazon product reviews (preprocessed) are used to generate answers

(In production, you can use embeddings or LLMs for smarter replies)

📸 Screenshots


📝 To Do
Integrate with real product QA models

Add session-based chat history

Deploy on Render/Heroku/Vercel

🙌 Acknowledgements
FastAPI

Bootstrap

Amazon Product Review Dataset

🧑‍💻 Author
Shahbaz Zulfiqar