import streamlit as st
from SL_agents import researcher, report_writer
from SL_tasks import icp_task, jtbd_task, pains_task
from langchain_openai import ChatOpenAI
from langsmith import traceable
from crewai import Crew, Process, Task
from fpdf import FPDF
import os
import smtplib
import logging
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pyairtable import Table

# Configure logging
logging.basicConfig(level=logging.INFO)

# Email configuration
SMTP_SERVER = 'smtpout.secureserver.net'
SMTP_PORT = 587
SENDER_EMAIL = 'info@swiftlaunch.biz'
SENDER_PASSWORD = 'Lovelife1#'

os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "SLwork8"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = "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"

# Airtable configuration
AIRTABLE_API_KEY = 'patnWOUVJR780iDNN.de9fb8264698287a5b4206fad59a99871d1fc6dddb4a94e7e7770ab3bcef014e'
AIRTABLE_BASE_ID = 'appPcWNUeei7MNMCj'
AIRTABLE_TABLE_NAME = 'tblaMtAcnVa4nwnby'
AIRTABLE_FIELDS = {
    'icp': 'JtbdfldFFAnoI7to8ZXgu',
    'jtbd': 'JtbdfldFFAnoI7to8ZXgu',
    'pains': 'PainsfldyazmtByhtLBEds'
}

table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)

@traceable
def send_to_airtable(email, icp_output, jtbd_output, pains_output):
    data = {
        "Email": email,
        AIRTABLE_FIELDS['icp']: icp_output,
        AIRTABLE_FIELDS['jtbd']: jtbd_output,
        AIRTABLE_FIELDS['pains']: pains_output,
    }
    try:
        record = table.create(data)
        logging.info("Airtable updated successfully")
        return record.get('id')
    except Exception as e:
        logging.error(f"Failed to update Airtable: {e}")
        return None

@traceable
def retrieve_from_airtable(record_id):
    try:
        record = table.get(record_id)
        fields = record.get('fields', {})
        logging.info("Data retrieved from Airtable successfully")
        return (
            fields.get(AIRTABLE_FIELDS['icp'], ''),
            fields.get(AIRTABLE_FIELDS['jtbd'], ''),
            fields.get(AIRTABLE_FIELDS['pains'], '')
        )
    except Exception as e:
        logging.error(f"Failed to retrieve data from Airtable: {e}")
        return None, None, None

@traceable
def start_crew_process(email, product_service, price, currency, payment_frequency, selling_scope, location):
    try:
        task_description = f"New task from {email} selling {product_service} at {price} {currency} with payment frequency {payment_frequency}."
        if selling_scope == "Locally":
            task_description += f" Location: {location}."
        
        new_task = Task(description=task_description, expected_output="...")
    
        project_crew = Crew(
            tasks=[new_task, icp_task, jtbd_task, pains_task],
            agents=[researcher, report_writer],
            manager_llm=ChatOpenAI(temperature=0, model="gpt-4"),
            max_rpm=8,
            process=Process.hierarchical,
            memory=True,
        )
        
        results = project_crew.kickoff()
    
        # Access task outputs directly
        icp_output = str(icp_task.output.exported_output)
        jtbd_output = str(jtbd_task.output.exported_output)
        pains_output = str(pains_task.output.exported_output)
    
        return icp_output, jtbd_output, pains_output
    except BrokenPipeError as e:
        logging.error(f"BrokenPipeError occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred during the crew process: {e}")
        raise

@traceable
def generate_pdf(icp_output, jtbd_output, pains_output):
    pdf = FPDF()
    pdf.add_page()
    
    # Set the title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="CrewAI Result", ln=True, align='C')
    
    # Add the ICP content
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="ICP Output", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, icp_output)
    
    # Add the JTBD content
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="JTBD Output", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, jtbd_output)
    
    # Add the Pains content
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Pains Output", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, pains_output)
    
    return pdf.output(dest="S").encode("latin1")

@traceable
def send_email(email, icp_output, jtbd_output, pains_output):
    pdf_content = generate_pdf(icp_output, jtbd_output, pains_output)
    
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
    logging.info("Email sent successfully")

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

        with st.spinner('Processing... please keep the page open for 5 minutes until you receive an email with the report'):
            try:
                icp_output, jtbd_output, pains_output = start_crew_process(email, product_service, price, currency, payment_frequency, selling_scope, location)
                record_id = send_to_airtable(email, icp_output, jtbd_output, pains_output)
                if record_id:
                    st.success("Airtable updated successfully!")

                    # Retrieve from Airtable using the record ID
                    retrieved_icp_output, retrieved_jtbd_output, retrieved_pains_output = retrieve_from_airtable(record_id)
                    
                    if retrieved_icp_output and retrieved_jtbd_output:
                        # Generate PDF
                        pdf_content = generate_pdf(retrieved_icp_output, retrieved_jtbd_output, retrieved_pains_output)
                        send_email(email, retrieved_icp_output, retrieved_jtbd_output, retrieved_pains_output)
                        st.success("The ICP has been generated and sent to your email.")
                        download_button(retrieved_icp_output, retrieved_jtbd_output, retrieved_pains_output)
                    else:
                        st.error("Failed to retrieve data from Airtable.")
                else:
                    st.error("Failed to update Airtable.")
            except Exception as e:
                logging.error(f"An error occurred: {e}")
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

def download_button(icp_output, jtbd_output, pains_output):
    pdf_content = generate_pdf(icp_output, jtbd_output, pains_output)

    st.download_button(
        label="Download Result as PDF",
        data=pdf_content,
        file_name='SwiftLaunch_ICP.pdf',
        mime='application/pdf',
    )

if __name__ == '__main__':
    main()
