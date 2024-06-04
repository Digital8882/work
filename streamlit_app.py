import streamlit as st
from SL_agents import researcher, report_writer
from SL_tasks import icp_task, jtbd_task, pains_task
from langchain_openai import ChatOpenAI
from langsmith import traceable
from crewai import Crew, Process, Task
from fpdf import FPDF
import os
import smtplib
import requests
import logging
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import traceback
from html.parser import HTMLParser
import builtins
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Email configuration
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587
SENDER_EMAIL = 'info@swiftlaunch.biz'
SENDER_PASSWORD = 'Lovelife1#'

os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "SL01"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = "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"

# Airtable configuration
AIRTABLE_API_KEY = 'patnWOUVJR780iDNN.de9fb8264698287a5b4206fad59a99871d1fc6dddb4a94e7e7770ab3bcef014e'
AIRTABLE_BASE_ID = 'appPcWNUeei7MNMCj'
AIRTABLE_TABLE_NAME = 'tblaMtAcnVa4nwnby'
AIRTABLE_FIELDS = {
    'icp': 'fldL1kkrGflCtOxwa',
    'jtbd': 'fldFFAnoI7to8ZXgu',
    'pains': 'fldyazmtByhtLBEds'
}

# Save the original print function
original_print = builtins.print

# Define a patched print function that logs instead of printing
def patched_print(*args, **kwargs):
    try:
        original_print(*args, **kwargs)
    except BrokenPipeError:
        logging.error(f"BrokenPipeError: {args}")
        logging.debug(traceback.format_exc())

# Patch the print function
builtins.print = patched_print

@traceable
def send_to_airtable(email, icp_output, jtbd_output, pains_output):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "Email": email,
            AIRTABLE_FIELDS['icp']: icp_output,
            AIRTABLE_FIELDS['jtbd']: jtbd_output,
            AIRTABLE_FIELDS['pains']: pains_output,
        }
    }
    try:
        logging.info(f"Sending data to Airtable: {data}")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        record = response.json()
        logging.info(f"Airtable response: {record}")
        return record['id']
    except Exception as e:
        logging.error(f"Failed to update Airtable: {e}")
        logging.debug(traceback.format_exc())
        return None

@traceable
def retrieve_from_airtable(record_id):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}/{record_id}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        record = response.json()
        logging.info(f"Retrieved from Airtable: {record}")
        return record['fields']
    except Exception as e:
        logging.error(f"Failed to retrieve from Airtable: {e}")
        logging.debug(traceback.format_exc())
        return None

# PDF class
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Swift Launch Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.ln(10)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def bullet_point(self, point):
        self.set_font('Arial', '', 12)
        self.cell(5)
        self.cell(0, 10, f"- {point}", 0, 1, 'L')

    def numbered_point(self, num, point):
        self.set_font('Arial', '', 12)
        self.cell(5)
        self.cell(0, 10, f"{num}. {point}", 0, 1, 'L')

# Function to generate PDF
def generate_pdf(data):
    pdf = PDF()
    pdf.add_page()
    for key, value in data.items():
        pdf.chapter_title(key)
        if isinstance(value, list):
            for item in value:
                pdf.bullet_point(item)
        else:
            pdf.chapter_body(value)
    pdf_file = 'Swift_Launch_Report.pdf'
    pdf.output(pdf_file)
    return pdf_file

def start_crew_process(email, product_service, price, currency, payment_frequency, selling_scope, location, retries=3):
    task_description = f"New task from {email} selling {product_service} at {price} {currency} with payment frequency {payment_frequency}."
    if selling_scope == "Locally":
        task_description += f" Location: {location}."
    # Add the logic to call the tasks (icp_task, jtbd_task, pains_task)
    # This is just a placeholder, replace it with actual task processing logic
    icp_output = "Ideal Customer Profile: Urban Eco-Rider\n- Age: 18-45\n- Gender: Both\n- Income: Middle to upper-middle class\n..."
    jtbd_output = "Jobs to be Done (JTBD):\n1. Commuting Efficiency\n2. Environmental Impact\n3. Cost-Effectiveness\n..."
    pains_output = "Customer Pains:\n1. High cost of traditional transportation\n2. Lack of eco-friendly options\n..."
    return icp_output, jtbd_output, pains_output

def send_email(recipient, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
        msg.attach(part)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    text = msg.as_string()
    server.sendmail(SENDER_EMAIL, recipient, text)
    server.quit()

# Streamlit application UI
def main():
    st.title("Swift Launch Report Generator")
    
    col1, col2 = st.columns(2)
    first_name = col1.text_input("First Name")
    email = col2.text_input("Email")

    if len(email) > 0 and "@" not in email:
        st.error("Please enter a valid email address")

    product_service = st.text_input("Product/Service being sold")
    
    col3, col4 = st.columns(2)
    price = col3.text_input("Price")
    currency = col4.selectbox("Currency", ["USD", "EUR", "GBP", "JPY", "AUD"])
    
    col5, col6 = st.columns(2)
    payment_frequency = col5.selectbox("Payment Frequency", ["One-time", "Monthly", "Yearly"])
    selling_scope = col6.selectbox("Are you selling Locally or Globally?", ["Locally", "Globally"])

    location = ""
    if selling_scope == "Locally":
        location = st.text_input("Location")

    if st.button("Submit"):
        if email and product_service and price:
            try:
                with st.spinner("Generating customer profile..."):
                    icp_output, jtbd_output, pains_output = start_crew_process(
                        email, product_service, price, currency, payment_frequency, selling_scope, location)
                
                record_id = send_to_airtable(email, icp_output, jtbd_output, pains_output)
                
                if record_id:
                    st.success("Data successfully sent to Airtable!")
                    
                    # Generate PDF
                    data = {
                        "ICP Output": icp_output,
                        "JTBD Output": jtbd_output,
                        "Pains Output": pains_output
                    }
                    pdf_file = generate_pdf(data)
                    
                    # Send email with PDF attachment
                    send_email(email, "Your Swift Launch Report", "Please find the attached report.", pdf_file)
                    st.success("Email sent successfully!")
                else:
                    st.error("Failed to send data to Airtable.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.error(traceback.format_exc())
                logging.error(f"An error occurred: {e}")
                logging.debug(traceback.format_exc())
        else:
            st.error("Please fill in all the required fields.")

if __name__ == "__main__":
    main()

# Restore the original print function after execution
builtins.print = original_print
