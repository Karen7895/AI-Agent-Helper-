# 🤖 Bannahyan AI Assistant

An **AI-powered personal assistant** designed to chat with website visitors, represent a professional identity,  
send automated welcome emails, and record unknown questions for later review.

Developed by **Karen Bannahyan**.

---

## 🧭 Overview

This project integrates **OpenAI**, **SendGrid**, and **Pushover** APIs to build an intelligent assistant that can:

- 💬 Chat with users in real time through a **Gradio** interface  
- 📧 Send automatic **welcome emails** when users provide their contact details  
- ✉️ Send **custom messages** to specific users  
- ❓ Log any **unknown or unanswered questions**  
- 🔔 Send **real-time push notifications** for key events (email success, error, or new contact)

---

## ⚙️ Main Features

### 1. AI Chat Interface
- Runs a **Gradio-based chat** window using the **OpenAI GPT-4o-mini** model.  
- Responds professionally as *"Karen Bannahyan"* using the content of `summary.txt`.

### 2. Automated Email System
- Uses **SendGrid API** to send:  
  - Welcome messages to new users  
  - Custom messages to specific email addresses  

### 3. Push Notifications
- Uses the **Pushover API** to send alerts when:  
  - A new user contact is recorded  
  - An email is sent successfully or fails  

### 4. Context Awareness
- Loads `summary.txt` to simulate Karen’s tone, experience, and professional knowledge.

### 5. Logging and Error Handling
- Automatically records unknown questions and errors via push alerts.

---

## 🧩 Tech Stack

- 🐍 Python 3.10+  
- 🧠 OpenAI API (chat and natural language responses)  
- ✉️ SendGrid API (email delivery)  
- 🔔 Pushover API (push notifications)  
- 💬 Gradio (chat UI)  
- ⚙️ dotenv (environment variable management)

---

## 🧰 Environment Setup

1. Create a `.env` file in the project folder with the following values:

   ```bash
   OPENAI_API_KEY=your_openai_key
   SENDGRID_API_KEY=your_sendgrid_key
   PUSHOVER_TOKEN=your_pushover_token
   PUSHOVER_USER=your_pushover_user
2. Create a `summary.txt` which includs information about owner
