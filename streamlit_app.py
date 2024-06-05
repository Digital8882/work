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
import builtins
import re
import urllib.parse  # For URL encoding
from html.parser import HTMLParser

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Email configuration
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587
SENDER_EMAIL = 'info@swiftlaunch.biz'
SENDER_PASSWORD = 'Lovelife1#'

os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "SL0j6llr9D1p0o"
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
        fields = record.get('fields', {})
        logging.info("Data retrieved from Airtable successfully")
        return (
            fields.get(AIRTABLE_FIELDS['icp'], ''),
            fields.get(AIRTABLE_FIELDS['jtbd'], ''),
            fields.get(AIRTABLE_FIELDS['pains'], '')
        )
    except Exception as e:
        logging.error(f"Failed to retrieve data from Airtable: {e}")
        logging.debug(traceback.format_exc())
        return None, None, None

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

    for attempt in range(retries):
        try:
            logging.info(f"Starting crew process, attempt {attempt + 1}")
            results = project_crew.kickoff()
            # Access task outputs directly
            icp_output = icp_task.output.exported_output if hasattr(icp_task.output, 'exported_output') else "No ICP output"
            jtbd_output = jtbd_task.output.exported_output if hasattr(jtbd_task.output, 'exported_output') else "No JTBD output"
            pains_output = pains_task.output.exported_output if hasattr(pains_task.output, 'exported_output') else "No Pains output"
            logging.info("Crew process completed successfully")
            return icp_output, jtbd_output, pains_output
        except BrokenPipeError as e:
            logging.error(f"BrokenPipeError occurred on attempt {attempt + 1}: {e}")
            logging.debug(traceback.format_exc())
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
        except Exception as e:
            logging.error(f"An error occurred during the crew process: {e}")
            logging.debug(traceback.format_exc())
            raise

class HTMLToPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_font("Arial", size=12)
        self.tag_stack = []

    def header(self):
        self.set_font("Arial", 'B', 12)
        self.set_text_color(255, 165, 0)
        self.cell(0, 10, 'Swift Launch Report', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_cover_page(self, title, subtitle, date):
        self.add_page()
        self.set_font("Arial", 'B', 24)
        self.cell(0, 10, title, 0, 1, 'C')
        self.ln(10)
        self.set_font("Arial", 'I', 16)
        self.cell(0, 10, subtitle, 0, 1, 'C')
        self.ln(20)
        self.set_font("Arial", 'I', 12)
        self.cell(0, 10, date, 0, 1, 'C')
        self.ln(20)

    def add_section(self, title, content, color):
        self.add_page()
        self.set_text_color(*color)  # Set color for the section line
        self.line(10, 10, 10, 287)  # Vertical line in the left margin
        self.set_text_color(0, 0, 0)  # Reset color for text
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)
        self.set_font("Arial", size=12)
        self.multi_cell(0, 10, content)

    def write_html(self, html):
        parser = HTMLParser()
        parser.handle_data = self.handle_data
        parser.handle_starttag = self.handle_starttag
        parser.handle_endtag = self.handle_endtag
        parser.feed(html)

    def handle_data(self, data):
        data = data.strip()
        if data and data != '`html':
            self.multi_cell(0, 7, txt=data)

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        if tag == 'b':
            self.set_font("Arial", 'B', size=12)
        elif tag == 'h1':
            self.set_font("Arial", 'B', size=16)
            self.ln(5)
        elif tag == 'h2':
            self.set_font("Arial", 'B', size=14)
            self.ln(5)
        elif tag == 'p':
            self.set_font("Arial", size=12)
        elif tag == 'table':
            self.set_font("Arial", size=12)
            self.ln(5)
        elif tag == 'th':
            self.set_font("Arial", 'B', size=12)
            self.cell(40, 10, 'Header', 1)
        elif tag == 'td':
            self.set_font("Arial", size=12)
            self.cell(40, 10, 'Cell', 1)

    def handle_endtag(self, tag):
        if tag in self.tag_stack:
            self.tag_stack.remove(tag)
        if tag in ['b', 'h1', 'h2']:
            self.set_font("Arial", size=12)
        if tag == 'p':
            self.ln(5)
        if tag == 'table':
            self.ln(10)
        if tag == 'th':
            self.ln(5)
        if tag == 'td':
            self.ln(5)

@traceable
def generate_pdf(icp_output, jtbd_output, pains_output):
    pdf = HTMLToPDF()
    
    # Add cover page
    pdf.add_cover_page(
        title="Swift Launch Report",
        subtitle="Customer Profile Analysis",
        date=datetime.now().strftime("%B %d, %Y")
    )
    
    # Process the outputs to remove unwanted markdown syntax
    icp_output_clean = icp_output.replace('```html', '').replace('```', '').strip()
    jtbd_output_clean = jtbd_output.replace('```html', '').replace('```', '').strip()
    pains_output_clean = pains_output.replace('```html', '').replace('```', '').strip()
    
    # Add ICP section
    pdf.add_section("ICP Output", icp_output_clean, (255, 0, 0))  # Red line
    
    # Add JTBD section
    pdf.add_section("JTBD Output", jtbd_output_clean, (0, 255, 0))  # Green line
    
    # Add Pains section
    pdf.add_section("Pains Output", pains_output_clean, (0, 0, 255))  # Blue line
    
    pdf_output = pdf.output(dest="S").encode("latin1")
    
    # Save a copy locally for inspection
    with open("report_debug.pdf", "wb") as f:
        f.write(pdf_output)
    
    return pdf_output

@traceable
def send_email(email, icp_output, jtbd_output, pains_output):
    pdf_content = generate_pdf(icp_output, jtbd_output, pains_output)  # Ensure all three arguments are passed
    
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
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        logging.debug(traceback.format_exc())

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

    st.markdown('<h1 class="title">Swift Launch Report</h1>', unsafe_allow_html=True)

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
                    send_email(email, icp_output, jtbd_output, pains_output)
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
