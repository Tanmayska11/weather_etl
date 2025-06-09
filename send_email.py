import yagmail
from dotenv import load_dotenv
import os



load_dotenv()

def send_email_notification(csv_file, receiver_email):
    # Your Gmail address and app password (NOT your normal Gmail password)
    sender_email = os.getenv('EMAIL')
    app_password = os.getenv('APP_PASSWORD')  # Generate this in Google Account > Security > App passwords

    subject = "Weather Data Updated"
    body = """
    Hi,

    The weather data CSV file has been updated. Please find the attached file.

    Best regards,
    Weather ETL
    """

    try:
        yag = yagmail.SMTP(user=sender_email, password=app_password)
        yag.send(
            to=receiver_email,
            subject=subject,
            contents=body,
            attachments=csv_file
        )
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


def send_email_notification_no_update(receiver_email):
    sender_email = os.getenv('EMAIL')
    app_password = os.getenv('APP_PASSWORD')

    subject = "Weather Data Not Updated"
    body = """
    Hi,

    The weather data CSV file has NOT been updated since the last check.

    Best regards,
    Weather ETL
    """
    try:
        yag = yagmail.SMTP(user=sender_email, password=app_password)
        yag.send(to=receiver_email, subject=subject, contents=body)
        print("✅ No-update email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send no-update email: {e}")
