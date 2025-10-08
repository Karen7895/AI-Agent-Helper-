from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
import gradio as gr
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

load_dotenv(override=True)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )

def send_email_to_user(user_email, subject, body):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("k@el-inter.net")
        to_email = To(user_email)
        content = Content("text/plain", body)
        mail = Mail(from_email, to_email, subject, content)
        
        mail_json = mail.get()
        response = sg.client.mail.send.post(request_body=mail_json)
        
        if response.status_code == 202:
            push(f"Email sent to {user_email} with subject: {subject}")
            return {"status": "success", "message": "Email sent successfully"}
        else:
            push(f"Failed to send email to {user_email}. Status: {response.status_code}")
            return {"status": "error", "message": f"Failed to send email: {response.status_code}"}
            
    except Exception as e:
        push(f"Error sending email to {user_email}: {str(e)}")
        return {"status": "error", "message": f"Error: {str(e)}"}

def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    
    # Auto-send welcome email when user provides email
    welcome_subject = "Welcome to Bannahyan AI Systems"
    welcome_body = f"""Dear {name if name != "Name not provided" else "Valued Client"},

Thank you for your interest in Bannahyan AI Systems. We specialize in advanced AI-driven solutions to help businesses optimize processes, improve compliance, and accelerate decision-making.

Our services include:
- AI-powered process optimization
- Automated compliance solutions
- Streamlined audit preparation
- Operational efficiency improvements

We'll be in touch shortly to discuss how we can help your business.

Best regards,
Karen Bannahyan
Bannahyan AI Systems
karenbannahyan@gmail.com
"""
    
    email_result = send_email_to_user(email, welcome_subject, welcome_body)
    return {"recorded": "ok", "email_sent": email_result["status"]}

def record_unknown_question(question):
    push(f"Recording unknown question: {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address. This will automatically send them a welcome email.",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

send_custom_email_json = {
    "name": "send_custom_email",
    "description": "Use this tool to send a custom email to a user with specific content",
    "parameters": {
        "type": "object",
        "properties": {
            "user_email": {
                "type": "string",
                "description": "The email address to send to"
            },
            "subject": {
                "type": "string",
                "description": "Subject of the email"
            },
            "body": {
                "type": "string",
                "description": "Body content of the email"
            }
        },
        "required": ["user_email", "subject", "body"],
        "additionalProperties": False
    }
}

def send_custom_email(user_email, subject, body):
    result = send_email_to_user(user_email, subject, body)
    return result

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
    {"type": "function", "function": send_custom_email_json}
]

class Me:
    def __init__(self):
        self.openai = OpenAI()
        self.name = "Karen Bannahyan"
        with open("summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        return results

    def system_prompt(self):
        system_prompt = (
            f"You are acting as {self.name}. You are answering questions on {self.name}'s website, "
            f"particularly questions related to {self.name}'s career, background, skills and experience. "
            f"Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. "
            f"You are given a summary of {self.name}'s background which you can use to answer questions. "
            f"Be professional and engaging, as if talking to a potential client or future employer who came across the website. "
            f"If you don't know the answer to any question, use your record_unknown_question tool to record it. "
            f"If the user is engaging in discussion, try to steer them towards getting in touch via email; "
            f"ask for their email and record it using your record_user_details tool (this will automatically send them a welcome email). "
            f"You can also use the send_custom_email tool to send specific information to users who provide their email."
        )

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools
            )
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content


if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()