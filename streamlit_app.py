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
os.environ["LANGSMITH_PROJECT"] = "SL31"
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

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Swift Launch Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.ln(10)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_subtitle(self, subtitle):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, subtitle, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def bullet_point(self, point):
        self.set_font('Arial', '', 12)
        self.cell(5)  # Indentation for bullet point
        self.cell(0, 10, f"- {point}", 0, 1, 'L')

    def numbered_point(self, num, point):
        self.set_font('Arial', '', 12)
        self.cell(5)  # Indentation for numbered point
        self.cell(0, 10, f"{num}. {point}", 0, 1, 'L')

def add_content_to_pdf(pdf, content):
    for section in content:
        if 'title' in section:
            pdf.chapter_title(section['title'])
        if 'subtitle' in section:
            pdf.chapter_subtitle(section['subtitle'])
        if 'body' in section:
            pdf.chapter_body(section['body'])
        if 'bullet_points' in section:
            for point in section['bullet_points']:
                pdf.bullet_point(point)
        if 'numbered_points' in section:
            for num, point in enumerate(section['numbered_points'], start=1):
                pdf.numbered_point(num, point)

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
            "ICP": icp_output,
            "JTBD": jtbd_output,
            "Pains": pains_output
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        record_id = response.json().get('id')
        return record_id
    else:
        logging.error(f"Failed to send data to Airtable: {response.status_code} - {response.text}")
        return None

def generate_pdf(email, icp_output, jtbd_output, pains_output):
    pdf = PDF()
    pdf.add_page()
    content = [
        {
            'title': 'ICP Output',
            'subtitle': f'Ideal Customer Profile for {email}',
            'body': icp_output
        },
        {
            'title': 'JTBD Output',
            'subtitle': 'Jobs to Be Done (JTBD) Analysis',
            'body': jtbd_output
        },
        {
            'title': 'Pains Output',
            'subtitle': 'Customer Pain Points',
            'body': pains_output
        }
    ]
    add_content_to_pdf(pdf, content)
    pdf_filename = f"{email}_report.pdf"
    pdf.output(pdf_filename)
    return pdf_filename

def send_email(recipient_email, pdf_filename):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = "Your Swift Launch Report"

    body = "Please find attached your Swift Launch report."
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(pdf_filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {pdf_filename}")

    msg.attach(part)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    text = msg.as_string()
    server.sendmail(SENDER_EMAIL, recipient_email, text)
    server.quit()

@traceable
def start_crew_process(email, product_service, price, currency, payment_frequency, selling_scope, location, retries=3):
    task_description = f"New task from {email} selling {product_service} at {price} {currency} with payment frequency {payment_frequency}."
    if selling_scope == "Locally":
        task_description += f" Location: {location}."
    
    new_task = Task(description=task_description, expected_output="...")

    project_crew = Crew(
        tasks=[new_task, icp_task, jtbd_task, pains_task],
        agents=[researcher, report_writer],
        manager_llm=ChatOpenAI(temperature=0, model="gpt-4o"),
        max_rpm=8,
        process=Process.hierarchical,
        memory=True,
    )

    # Assuming this function returns the outputs directly for the sake of example
    icp_output = "Generated ICP output here"
    jtbd_output = "Generated JTBD output here"
    pains_output = "Generated Pains output here"

    return icp_output, jtbd_output, pains_output

def main():
    st.title("Swift Launch")
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
                    pdf_filename = generate_pdf(email, icp_output, jtbd_output, pains_output)
                    st.success("PDF generated successfully!")
                    send_email(email, pdf_filename)
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
