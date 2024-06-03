import streamlit as st
from SL_agents import researcher, report_writer
from SL_tasks import icp_task
from langchain_openai import ChatOpenAI
from crewai import Crew, Process, Task
from fpdf import FPDF
import io
import os
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests

# Email configuration
SMTP_SERVER = 'smtpout.secureserver.net'
SMTP_PORT = 587
SENDER_EMAIL = 'info@swiftlaunch.biz'
SENDER_PASSWORD = 'Lovelife1#'

# Airtable configuration
AIRTABLE_API_KEY = 'patnWOUVJR780iDNN.de9fb8264698287a5b4206fad59a99871d1fc6dddb4a94e7e7770ab3bcef014e'
AIRTABLE_BASE_ID = 'appPcWNUeei7MNMCj'
AIRTABLE_TABLE_NAME = 'tblaMtAcnVa4nwnby'
AIRTABLE_FIELD_ID = 'fldsx1iIk4FiRaLi8'

# File to store user access records
USER_RECORDS_FILE = "user_records.json"

def load_user_records():
    if os.path.exists(USER_RECORDS_FILE):
        with open(USER_RECORDS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_user_records(records):
    with open(USER_RECORDS_FILE, "w") as file:
        json.dump(records, file)

def can_generate_icp(email):
    records = load_user_records()
    if email in records:
        last_generated = datetime.fromisoformat(records[email])
        if datetime.now() - last_generated < timedelta(days=1):
            return False
    return True

def update_user_record(email):
    records = load_user_records()
    records[email] = datetime.now().isoformat()
    save_user_records(records)

def send_to_airtable(email, opt_in):
    url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'
    headers = {
        'Authorization': f'Bearer {AIRTABLE_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'records': [
            {
                'fields': {
                    'Email': email,
                    'Opt-in': opt_in
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

def start_crew_process(email, product_service, price, currency, payment_frequency, selling_scope, location):
    task_description = f"New task from {email} selling {product_service} at {price} {currency} with payment frequency {payment_frequency}."
    if selling_scope == "Locally":
        task_description += f" Location: {location}."
    
    new_task = Task(description=task_description, expected_output="...")

    project_crew = Crew(
        tasks=[new_task, icp_task],
        agents=[researcher, report_writer],
        manager_llm=ChatOpenAI(temperature=0, model="gpt-4o"),
        max_rpm=2,
        process=Process.hierarchical,
        memory=True,
    )
    
    result = project_crew.kickoff()
    return result

def generate_pdf(result):
    pdf = FPDF()
    pdf.add_page()
    
    # Set the title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="CrewAI Result", ln=True, align='C')
    
    # Add the result content with better formatting
    pdf.set_font("Arial", size=12)
    
    # Split the result by lines
    lines = result.split('\n')
    
    for line in lines:
        if "**" in line:  # Detect headings and subheadings
            pdf.set_font("Arial", 'B', 12)
            line = line.replace("**", "")
        else:
            pdf.set_font("Arial", size=12)
        
        pdf.multi_cell(0, 8, line.strip())  # Use tighter line spacing
    
    return pdf.output(dest="S").encode("latin1")

def send_email(email, result):
    pdf_content = generate_pdf(result)
    
    # Email details
    subject = 'Swift Launch ICP'
    body = 'Please find attached the result Ideal customer profile.'
    
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg['Subject'] = subject
    
    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the PDF file
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(pdf_content)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename=crewAI_result.pdf')
    msg.attach(attachment)
    
    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, msg.as_string())

def main():
    # Inject custom CSS for dynamic iframe height adjustment and hiding Streamlit branding
    st.markdown(
        """
        <style>
        @import url('style.css');
        .stApp {
            background-color: #000000;
        }
        .title {
            color: #DE6A1D;
            font-size: 3em;
        }
        .subtitle {
            color: #DE6A1D;
            font-size: 1.2em;
        }
        input {
            background-color: #1A1A1A !important;
            color: #FFFFFF !important;
        }
        textarea {
            background-color: #1A1A1A !important;
            color: #FFFFFF !important;
        }
        select {
            background-color: #1A1A1A !important;
            color: #FFFFFF !important;
        }
        footer {visibility: hidden;}
        .css-1v0mbdj {padding-top: 0 !important;}
        .block-container {padding-top: 20px !important;}
        .stApp a:first-child {display: none;}
        .css-15zrgzn {display: none;}
        .css-eczf16 {display: none;}
        .css-jn99sy {display: none;}
        div[data-testid="stToolbar"] { display: none; }
        </style>
        <script>
        function sendHeight() {
            const height = document.documentElement.scrollHeight;
            window.parent.postMessage({ height: height }, '*');
        }

        window.addEventListener('load', sendHeight);
        window.addEventListener('resize', sendHeight);
        </script>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<h1 class="title">Ideal Customer Profile Generator</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    first_name = col1.text_input("First Name")
    email = col2.text_input("Email")

    if len(email) > 0 and "@" not in email:
        st.error("Please enter a valid email address")

    product_service = st.text_input("Product/Service being sold")
    
    col1, col2 = st.columns(2)
    price = col1.number_input("Price", min_value=0, step=1, format="%d")
    currency = col2.selectbox("Currency", ["USD", "EUR", "GBP", "INR", "AUD", "CAD", "JPY", "CNY", "Other"])
    
    payment_frequency = st.selectbox("Payment Frequency", ["Select an option", "One-time", "Daily", "Weekly", "Monthly", "Quarterly", "Annually"])
    
    col1, col2 = st.columns(2)
    selling_scope = col1.selectbox("Selling Scope", ["Select an option", "Locally", "Nationally", "Internationally"])
    location = col2.text_input("Location (if selling locally)")

    opt_in = st.checkbox('Allow Swift Launch to send me valuable content (we will never share your data)', value=True)

    if st.button("Submit"):
        if not validate_input(email, product_service, price, payment_frequency, selling_scope, location):
            st.error("Please fill in all fields correctly.")
            return

        if not can_generate_icp(email):
            st.warning("You have already generated a report today. Please try again tomorrow.")
            return

        with st.spinner('Processing... please keep the page open for 5 minutes until you receive an email with the report'):
            try:
                result = start_crew_process(email, product_service, price, currency, payment_frequency, selling_scope, location)
                update_user_record(email)
                send_to_airtable(email, opt_in)
                send_email(email, result)
                st.success("The ICP has been generated and sent to your email.")
                download_button(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")

def validate_input(email, product_service, price, payment_frequency, selling_scope, location):
    if "@" not in email or len(email) == 0:
        return False
    if len(product_service) == 0:
        return False
    if price <= 0:
        return False
    if payment_frequency == "Select an option":
        return False
    if selling_scope == "Select an option":
        return False
    if selling_scope == "Locally" and len(location) == 0:
        return False
    return True

def download_button(result):
    pdf_content = generate_pdf(result)

    st.download_button(
        label="Download Result as PDF",
        data=pdf_content,
        file_name='SwiftLaunch_ICP.pdf',
        mime='application/pdf',
    )

if __name__ == '__main__':
    main()
