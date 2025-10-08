Bannahyan AI Assistant
======================

An AI-powered personal assistant designed to chat with website visitors, represent a professional identity,
send automated welcome emails, and record unknown questions for later review.

Developed by Karen Bannahyan.


------------------------------------------------------------
Overview
------------------------------------------------------------

This project integrates OpenAI, SendGrid, and Pushover APIs to build an intelligent assistant
that can:

- Chat with users in real time through a Gradio interface
- Send automatic welcome emails when users provide their contact details
- Send custom messages to specific users
- Log any unknown or unanswered questions
- Send real-time push notifications for key events (email success, error, or new contact)


------------------------------------------------------------
Main Features
------------------------------------------------------------

1. AI Chat Interface
   - Runs a Gradio-based chat window using the OpenAI GPT-4o-mini model.
   - Responds professionally as "Karen Bannahyan" based on the contents of summary.txt.

2. Automated Email System
   - Uses SendGrid API to send:
     • Welcome messages to new users
     • Custom messages to specific email addresses

3. Push Notifications
   - Uses the Pushover API to send alerts when:
     • A new user contact is recorded
     • An email is sent successfully or fails

4. Context Awareness
   - Loads summary.txt file to simulate Karen’s tone, experience, and professional knowledge.

5. Logging and Error Handling
   - Automatically records unknown questions and errors via push alerts.


------------------------------------------------------------
Tech Stack
------------------------------------------------------------

- Python 3.10+
- OpenAI API (for chat and natural language responses)
- SendGrid API (for email delivery)
- Pushover API (for push notifications)
- Gradio (for chat UI)
- dotenv (for environment variables)


------------------------------------------------------------
Environment Setup
------------------------------------------------------------

1. Create a .env file in the project folder with the following values:

   OPENAI_API_KEY=your_openai_key
   SENDGRID_API_KEY=your_sendgrid_key
   PUSHOVER_TOKEN=your_pushover_token
   PUSHOVER_USER=your_pushover_user

2. Install dependencies:

   pip install -r requirements.txt


------------------------------------------------------------
Running the Application
------------------------------------------------------------

Start the assistant locally by running:

   python main.py

After launching, a local Gradio link will appear in the console.
Open that link in your browser to start chatting with the assistant.


------------------------------------------------------------
File Structure
------------------------------------------------------------

main.py          - Main script containing chat logic and AI behavior
summary.txt      - Persona summary used to shape responses
.env              - Environment configuration (not shared publicly)
requirements.txt - Python dependencies


------------------------------------------------------------
Available Tools / Functions
------------------------------------------------------------

1. record_user_details
   Records a user's email, name, and notes.
   Automatically sends a welcome email.

2. record_unknown_question
   Logs any question that the assistant could not answer.

3. send_custom_email
   Sends a custom email to a specified user.

Each of these tools can be called by the AI when certain conditions are met.


------------------------------------------------------------
Use Cases
------------------------------------------------------------

- Personal AI chatbot for a portfolio or business website
- Automated lead collection and follow-up
- Email onboarding assistant
- Customer support and Q&A assistant


------------------------------------------------------------
Author
------------------------------------------------------------

Karen Bannahyan
Bannahyan AI Systems
Email: karenbannahyan@gmail.com


------------------------------------------------------------
License
------------------------------------------------------------

This project is provided for educational and personal portfolio purposes.
Use responsibly and ensure API keys are kept private.
