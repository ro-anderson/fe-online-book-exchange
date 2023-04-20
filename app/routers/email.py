from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import smtplib
from email.message import EmailMessage

router = APIRouter()

class EmailContent(BaseModel):
    recipient_email: str
    message: str

@router.post("/send-email")
async def send_email(email_content: EmailContent):
    YOUR_EMAIL = "trocanaescola@gmail.com"
    YOUR_PASSWORD = "usnrhziopoojvqdn"

    msg = EmailMessage()
    msg.set_content(email_content.message)
    print(f"email content:\n {email_content}")

    msg["Subject"] = "Alguém tem interesse no seu livro 👀 [Troca na Escola]"
    msg["From"] = YOUR_EMAIL
    msg["To"] = email_content.recipient_email

    try:
        print("Attempting to connect to SMTP server...")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        print("Connected. Attempting to log in...")
        server.login(YOUR_EMAIL, YOUR_PASSWORD)
        print("Logged in. Attempting to send email...")
        server.send_message(msg)
        print("Email sent. Quitting server...")
        server.quit()
        return {"success": True}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        

if __name__ == "__main__":
    print(dir())