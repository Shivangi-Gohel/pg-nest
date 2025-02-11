import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
import os

SMTP_SERVER = "smtp.gmail.com"  # Replace with your SMTP server
SMTP_PORT = 587  # Standard port for TLS
SENDER_EMAIL = "your_email@gmail.com"  # Replace with your sender email
SENDER_PASSWORD = "your_password"  # Replace with your email password (use app password for Gmail)

def send_checkout_email(user_email, user_id, amount, receipt_path):
    try:
        # Create the email object
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = user_email
        msg["Subject"] = "PG-Nest: Payment Receipt & Checkout Confirmation"

        # HTML content for the email
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #4CAF50;">PG-Nest: Payment Receipt</h2>
            <p>Dear Guest,</p>
            <p>Thank you for staying with <strong>PG-Nest</strong>. Here are your checkout details:</p>
            <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
                <tr style="background-color: #f0f0f0;">
                    <th style="text-align: left;">User ID</th>
                    <td>{user_id}</td>
                </tr>
                <tr>
                    <th style="text-align: left;">Amount Paid</th>
                    <td>{amount} INR</td>
                </tr>
                <tr>
                    <th style="text-align: left;">Date</th>
                    <td>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</td>
                </tr>
            </table>
            <p>You can find your receipt attached to this email.</p>
            <p>We hope to see you again soon!</p>
            <p style="color: #555;">--<br>PG-Nest Team</p>
        </body>
        </html>
        """

        # Attach the HTML content to the email
        msg.attach(MIMEText(html_content, "html"))

        # Attach the receipt file
        with open(receipt_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(receipt_path)}",
            )
            msg.attach(part)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"Email sent successfully to {user_email}.")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
