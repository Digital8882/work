import re
from fpdf import FPDF
import streamlit as st
import logging
import asyncio
import httpx
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from langchain_openai import ChatOpenAI
from crewai import Crew, Process, Task
from SL_agents import researcher, report_writer
from SL_tasks import icp_task, jtbd_task, pains_task
from langsmith import traceable
import os
import builtins
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Email configuration
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587
SENDER_EMAIL = 'info@swiftlaunch.biz'
SENDER_PASSWORD = 'Lovelife1#'

os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "SL0l6l944p0o"
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
async def send_to_airtable(email, icp_output, jtbd_output, pains_output, retries=3):
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
    async with httpx.AsyncClient() as client:
        for attempt in range(retries):
            try:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()
                record = response.json()
                logging.info(f"Airtable response: {record}")
                return record['id']
            except httpx.HTTPStatusError as e:
                logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            except httpx.RequestError as e:
                logging.error(f"Request error occurred: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    raise Exception("Failed to send data to Airtable after multiple attempts")

@traceable
async def retrieve_from_airtable(record_id, retries=3):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}/{record_id}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    async with httpx.AsyncClient() as client:
        for attempt in range(retries):
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                record = response.json()
                fields = record.get('fields', {})
                logging.info("Data retrieved from Airtable successfully")
                return (
                    fields.get(AIRTABLE_FIELDS['icp'], ''),
                    fields.get(AIRTABLE_FIELDS['jtbd'], ''),
                    fields.get(AIRTABLE_FIELDS['pains'], '')
                )
            except httpx.HTTPStatusError as e:
                logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            except httpx.RequestError as e:
                logging.error(f"Request error occurred: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    raise Exception("Failed to retrieve data from Airtable after multiple attempts")

@traceable
async def start_crew_process(email, product_service, price, currency, payment_frequency, selling_scope, location, retries=3):
    task_description = f"New task from {email} selling {product_service} at {price} {currency} with payment frequency {payment_frequency}."
    if selling_scope == "Locally":
        task_description += f" Location: {location}."

    new_task = Task(description=task_description, expected_output="...")

    project_crew = Crew(
        tasks=[new_task, icp_task, jtbd_task, pains_task],
        agents=[researcher, report_writer],
        manager_llm=ChatOpenAI(temperature=0, model="gpt-4o"),
        max_rpm=4,
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

class RichTextPDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 12)
        self.set_text_color(255, 165, 0)  # Orange color
        self.cell(0, 10, 'Swift Launch Report', 0, 1, 'R')
        self.ln(10)

    def write_rich_text(self, text):
        lines = text.split('\n')
        for line in lines:
            if line.startswith('# '):
                self.set_font('Arial', 'B', 16)
                self.multi_cell(0, 10, line[2:])
            elif line.startswith('## '):
                self.set_font('Arial', 'B', 14)
                self.multi_cell(0, 10, line[3:])
            elif line.startswith('### '):
                self.set_font('Arial', 'B', 12)
                self.multi_cell(0, 10, line[4:])
            elif line.startswith('- '):
                self.set_font('Arial', '', 12)
                self.cell(10)
                self.multi_cell(0, 10, '- ' + line[2:])
            else:
                self.write_formatted_text(line)
            self.ln(5)

    def write_formatted_text(self, text):
        segments = self.parse_inline_formatting(text)
        for segment in segments:
            if segment[0] == 'bold':
                self.set_font('Arial', 'B', 12)
            elif segment[0] == 'italic':
                self.set_font('Arial', 'I', 12)
            else:
                self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, segment[1], 0, 'L', False)

    def parse_inline_formatting(self, text):
        segments = []
        pos = 0
        while True:
            bold_match = re.search(r'\*\*(.*?)\*\*', text, pos)
            italic_match = re.search(r'\*(.*?)\*', text, pos)
            if not bold_match and not italic_match:
                segments.append(('normal', text[pos:]))
                break
            if bold_match and (not italic_match or bold_match.start() < italic_match.start()):
                if bold_match.start() > pos:
                    segments.append(('normal', text[pos:bold_match.start()]))
                segments.append(('bold', bold_match.group(1)))
                pos = bold_match.end()
            else:
                if italic_match.start() > pos:
                    segments.append(('normal', text[pos:italic_match.start()]))
                segments.append(('italic', italic_match.group(1)))
                pos = italic_match.end()
        return segments

# Example of generating the PDF
def generate_pdf(icp_output, jtbd_output, pains_output):
    pdf = RichTextPDF()
    
    pdf.add_page()
    
    pdf.write_rich_text(f"# ICP Output\n\n{icp_output}\n\n")
    pdf.ln(10)
    pdf.write_rich_text(f"# JTBD Output\n\n{jtbd_output}\n\n")
    pdf.ln(10)
    pdf.write_rich_text(f"# Pains Output\n\n{pains_output}\n\n")
    
    pdf_output = pdf.output(dest="S").encode("latin1")
    
    # Save a copy locally for inspection
    with open("report_debug.pdf", "wb") as f:
        f.write(pdf_output)
    
    return pdf_output

def send_email_with_retry(email, icp_output, jtbd_output, pains_output, retries=3, delay=5):
    logging.info("Generating PDF content")
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
    
    for attempt in range(retries):
        try:
            logging.info(f"Attempt {attempt + 1}: Connecting to SMTP server")
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                logging.info("Logging in to SMTP server")
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                logging.info("Sending email")
                server.sendmail(SENDER_EMAIL, email, msg.as_string())
            logging.info("Email sent successfully")
            return True
        except smtplib.SMTPException as e:
            logging.error(f"SMTP error on attempt {attempt + 1}: {e}")
        except Exception as e:
            logging.error(f"General error on attempt {attempt + 1}: {e}")
            logging.debug(traceback.format_exc())
        time.sleep(delay)
    return False

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
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    icp_output, jtbd_output, pains_output = loop.run_until_complete(
                        start_crew_process(
                            email, product_service, price, currency, payment_frequency, selling_scope, location
                        )
                    )

                    record_id = loop.run_until_complete(
                        send_to_airtable(email, icp_output, jtbd_output, pains_output)
                    )
                    
                    if record_id:
                        st.success("Data successfully sent to Airtable!")
                        if send_email_with_retry(email, icp_output, jtbd_output, pains_output):
                            st.success("Email sent successfully!")
                        else:
                            st.error("Failed to send email after multiple attempts.")
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

