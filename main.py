from fastapi import FastAPI, Form
import mysql.connector
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

db = mysql.connector.connect(
    host="sql305.infinityfree.com",
    user="if0_40489081",
    password="piyush@123",
    database="if0_40489081_cropdb"
)
cursor = db.cursor()

def send_email(name, email):
    sender = "piyushradhe14@gmail.com"
    password = "szxi wyoqxjsz btrf"

    msg = MIMEText(f"New User Registered:\nName: {name}\nEmail: {email}")
    msg['Subject'] = "New Account Created"
    msg['From'] = sender
    msg['To'] = sender

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender, password)
    server.sendmail(sender, sender, msg.as_string())
    server.quit()

@app.post("/signup")
def signup(name: str = Form(), email: str = Form(), password: str = Form()):
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, password)
    )
    db.commit()
    send_email(name, email)
    return {"message": "Account Created Successfully"}

@app.post("/login")
def login(email: str = Form(), password: str = Form()):
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    if not user:
        return {"message": "Invalid Credentials"}
    return {"message": "Login Successful", "user": user}
