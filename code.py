import google.generativeai as genai
genai.configure(api_key="AIzaSyC2z6eCS_SXX03QIKz3nA15biwKGXvUy08")
model = genai.GenerativeModel('gemini-pro')
import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Set your email and password
#this is the main company email
email_address = "admin@funkaary.com"
password = "Shlok007"

# Connect to the IMAP server (for Gmail, use 'imap.gmail.com')
mail = imaplib.IMAP4_SSL('imap.gmail.com')

# Log in to your account
mail.login(email_address, password)

# Infinite loop to continuously monitor the email inbox
while True:
    try:
        # Select the mailbox you want to read (e.g., 'inbox')
        mail.select("inbox")

        # Search for unread emails in the selected mailbox
        status, messages = mail.search(None, "UNSEEN")
        message_ids = messages[0].split()

        # Check if there are any unread emails
        if not message_ids:
            print("No unread messages.")
            time.sleep(60)  # Wait for 60 seconds before checking again
            continue

        # Loop through each unread email
        for message_id in message_ids:
            # Fetch the unread email
            status, msg_data = mail.fetch(message_id, "(RFC822)")
            if status != 'OK':
                print("Error fetching message:", message_id)
                continue

            raw_email = msg_data[0][1]

            # Decode the raw email bytes to a string
            raw_email_string = raw_email.decode("utf-8")

            # Parse the raw email using the email library
            msg = email.message_from_string(raw_email_string)

            # Extract information from the email
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            email_body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        email_body = part.get_payload(decode=True).decode()
                        break
            else:
                email_body = msg.get_payload(decode=True).decode()

            response = model.generate_content(f"classify this email as complaint, query or request : {email_body}")

            # Perform classification on the email body (Replace this with your classification logic)
            # For demonstration, let's assume the body contains keywords "complaint" or "query" or" "request" these are the names of the departments
            if "complaint" in (response.text).lower():
                to_address = "godshlok2011@gmail.com"
            elif "query" in (response.text).lower():
                to_address = "rameshrajni2011@gmail.com"
            elif "request" in (response.text).lower():
                to_address = "goelshlok2011@gmail.com"
            else:
                print("Could not classify the email. No action taken.")
                continue

            # Create a MIME message for forwarding
            forwarded_msg = MIMEMultipart()
            forwarded_msg["From"] = email_address
            forwarded_msg["To"] = to_address
            forwarded_msg["Subject"] = subject

            # Add the original email as an attachment
            forwarded_msg.attach(MIMEText(raw_email_string, "plain"))

            # Send the email using SMTP
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_address, password)
                smtp.sendmail(email_address, to_address, forwarded_msg.as_string())
                print("Email forwarded successfully to:", to_address)

            # Mark the email as read (optional)
            mail.store(message_id, '+FLAGS', '\Seen')

    except Exception as e:
        print("An error occurred:", e)

# Logout from the server
mail.logout()