import streamlit as st
from SL_agents import researcher, analyst, profiler, strategist  # Updated agents
from SL_tasks import task_market_research, task_data_analysis ,task_persona_development, task_strategy_recommendations, task_final_report
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
import time
import traceback
import builtins
import re
import asyncio
import httpx

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Email configuration
SMTP_SERVER = 'mail.privateemail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'yourorder@swiftlaunch.biz'
SENDER_PASSWORD = 'Lovelife1#'



os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "SL0llu1p0o"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")  # Securely fetch

# Airtable configuration


# Save the original print function
original_print = builtins.print

@traceable
async def start_crew_process(business_info, product_service, price, currency, payment_frequency, selling_scope, location, icp_info, retries=3):
    task_description = f"New task from {business_info.get('email')} for the product/service '{product_service.get('name')}' priced at {price} {currency}. Location: {location}."
    if selling_scope == "Locally":
        task_description += f" Selling locally in {location}."
    else:
        task_description += " Selling globally."



    # Initialize the Crew with updated configurations
    project_crew = Crew(
        tasks=[
            task_market_research(business_info, product_service, price, currency, payment_frequency, selling_scope, location, icp_info),
            task_data_analysis(),
            task_persona_development(),
            task_strategy_recommendations(),
            task_final_report(business_info, product_service, price, currency, payment_frequency, selling_scope, location)
        ],
        agents=[researcher, analyst, profiler, strategist],
        manager_llm=ChatOpenAI(temperature=0, model="gpt-4o-2024-08-06"), # Updated line: Pass model name as string
        process=Process.hierarchical,
        respect_context_window=True,
        memory=True,
        manager_agent=None,
        planning=True,
    )

    for attempt in range(retries):
        try:
            logging.info(f"Starting crew process, attempt {attempt + 1}")
            results = project_crew.kickoff()
            # Access task outputs directly
            market_research_output = results.get('task_market_research', "No Market Research output")
            data_analysis_output = results.get('task_data_analysis', "No Data Analysis output")
            persona_development_output = results.get('task_persona_development', "No Persona Development output")
            strategy_recommendations_output = results.get('task_strategy_recommendations', "No Strategy Recommendations output")
            final_report_output = results.get('task_final_report', "No Final Report output")
            logging.info("Crew process completed successfully")
            return (
                market_research_output,
                data_analysis_output,
                persona_development_output,
                strategy_recommendations_output,
                final_report_output
            )
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


    for attempt in range(retries):
        try:
            logging.info(f"Starting crew process, attempt {attempt + 1}")
            results = project_crew.kickoff()
            # Access task outputs directly
            market_research_output = results.get('task_market_research', "No Market Research output")
            data_analysis_output = results.get('task_data_analysis', "No Data Analysis output")
            persona_development_output = results.get('task_persona_development', "No Persona Development output")
            strategy_recommendations_output = results.get('task_strategy_recommendations', "No Strategy Recommendations output")
            final_report_output = results.get('task_final_report', "No Final Report output")
            logging.info("Crew process completed successfully")
            return (
                market_research_output,
                data_analysis_output,
                persona_development_output,
                strategy_recommendations_output,
                final_report_output
            )
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

@traceable
def format_output(output):
    formatted_output = ""
    sections = output.split("\n\n")
    for section in sections:
        lines = section.split("\n")
        if lines:
            header = lines[0].strip()
            content_lines = []
            for line in lines[1:]:
                stripped_line = line.strip()
                if stripped_line.startswith("-"):
                    content_lines.append(stripped_line)
                else:
                    if content_lines:
                        content_lines[-1] += " " + stripped_line
                    else:
                        content_lines.append(stripped_line)
            content = "\n".join(content_lines)
            formatted_output += f"{header}\n{content}\n\n"
    return formatted_output.strip()

@traceable
def generate_pdf(
    market_research_output,
    data_analysis_output,
    persona_development_output,
    strategy_recommendations_output,
    final_report_output,
    font_name="Courier",
    custom_font=False
):
    pdf = FPDF()
    pdf.add_page()

    if custom_font:
        # Add regular and bold variants of the custom font
        pdf.add_font(font_name, style="", fname=f"{font_name}.ttf")
        pdf.add_font(font_name, style="B", fname=f"{font_name}-Bold.ttf")

    pdf.set_font(font_name, size=12)  # Use the specified font

    market_research_output = format_output(market_research_output)
    data_analysis_output = format_output(data_analysis_output)
    persona_development_output = format_output(persona_development_output)
    strategy_recommendations_output = format_output(strategy_recommendations_output)
    final_report_output = format_output(final_report_output)

    def add_markdown_text(pdf, text):
        lines = text.split('\n')
        for line in lines:
            if line.startswith('###'):
                pdf.set_font(font_name, style='B', size=16)
                pdf.multi_cell(0, 10, line[3:].strip())
            elif line.startswith('##'):
                pdf.set_font(font_name, style='B', size=14)
                pdf.multi_cell(0, 10, line[2:].strip())
            elif line.startswith('#'):
                pdf.set_font(font_name, style='B', size=12)
                pdf.multi_cell(0, 10, line[1:].strip())
            elif line.startswith('-'):
                pdf.set_font(font_name, style='')
                pdf.cell(0, 10, line.strip(), ln=1)
            else:
                bold_parts = re.split(r'(\*\*.*?\*\*)', line)
                for part in bold_parts:
                    if part.startswith('**') and part.endswith('**'):
                        pdf.set_font(font_name, style='B')
                        pdf.multi_cell(0, 5, part[2:-2])
                    else:
                        pdf.set_font(font_name, style='')
                        pdf.multi_cell(0, 5, part)
            pdf.ln(2.5)  # Reduce space between lines to 50%

    # Add Market Research output
    pdf.multi_cell(0, 10, "Market Research Output:")
    add_markdown_text(pdf, market_research_output)

    # Add new page for Data Analysis output
    pdf.add_page()
    pdf.multi_cell(0, 10, "Data Analysis Output:")
    add_markdown_text(pdf, data_analysis_output)

    # Add new page for Persona Development output
    pdf.add_page()
    pdf.multi_cell(0, 10, "Persona Development Output:")
    add_markdown_text(pdf, persona_development_output)

    # Add new page for Strategy Recommendations output
    pdf.add_page()
    pdf.multi_cell(0, 10, "Strategy Recommendations Output:")
    add_markdown_text(pdf, strategy_recommendations_output)

    # Add new page for Final Report
    pdf.add_page()
    pdf.multi_cell(0, 10, "Final Report:")
    add_markdown_text(pdf, final_report_output)

    pdf_output = pdf.output(dest="S").encode("latin1")

    with open("report_debug.pdf", "wb") as f:
        f.write(pdf_output)

    return pdf_output

@traceable
def send_email(email, market_research_output, data_analysis_output, persona_development_output, strategy_recommendations_output, final_report_output, retries=3):
    pdf_content = generate_pdf(
        market_research_output,
        data_analysis_output,
        persona_development_output,
        strategy_recommendations_output,
        final_report_output
    )  # Ensure all five arguments are passed

    # Email details
    subject = 'Swift Launch ICP Report'
    body = 'Please find attached the comprehensive Ideal Customer Profile (ICP) report.'

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
    attachment.add_header('Content-Disposition', f'attachment; filename=ICP_Report.pdf')
    msg.attach(attachment)

    for attempt in range(retries):
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, email, msg.as_string())
            logging.info("Email sent successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to send email on attempt {attempt + 1}: {e}")
            logging.debug(traceback.format_exc())
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
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

    st.markdown('<h1 class="title">Swift Launch ICP Report</h1>', unsafe_allow_html=True)

    st.subheader("Enter Your Business and Product Details")

    # Collect Business Information
    business_info = {}
    business_info['name'] = st.text_input("Business Name", placeholder="Enter your business name")
    business_info['description'] = st.text_area("Business Description", placeholder="Describe your business")
    business_info['unique_value_proposition'] = st.text_area("Unique Value Proposition", placeholder="What makes your business unique?")
    business_info['email'] = st.text_input("Contact Email", placeholder="Enter your contact email")

    st.markdown("---")

    # Collect Product/Service Information
    product_service = {}
    product_service['name'] = st.text_input("Product/Service Name", placeholder="Enter the name of your product or service")
    product_service['features'] = st.text_area("Features", placeholder="List the features of your product/service (separated by commas)")
    product_service['benefits'] = st.text_area("Benefits", placeholder="List the benefits of your product/service (separated by commas)")

    st.markdown("---")

    # Collect Pricing and Location Information
    col1, col2 = st.columns(2)
    price = col1.text_input("Price", placeholder="Enter the price")
    currency = col2.selectbox("Currency", ["USD", "EUR", "GBP", "JPY", "AUD"])

    col3, col4 = st.columns(2)
    payment_frequency = col3.selectbox("Payment Frequency", ["One-time", "Monthly", "Yearly"])
    selling_scope = col4.selectbox("Are you selling Locally or Globally?", ["Locally", "Globally"])

    location = ""
    if selling_scope == "Locally":
        location = st.text_input("Location", placeholder="Enter your selling location")

    st.markdown("---")

    # Collect Known Information on ICP
    icp_info = st.text_area("Known Information on Ideal Customer Profile (ICP)", placeholder="Provide any known information about your ideal customers")

    if st.button("Submit"):
        if (
            business_info['name'] and
            business_info['description'] and
            business_info['unique_value_proposition'] and
            business_info['email'] and
            product_service['name'] and
            product_service['features'] and
            product_service['benefits'] and
            price and
            (selling_scope == "Globally" or location) and
            icp_info
        ):
            try:
                with st.spinner("Generating Ideal Customer Profile..."):
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                    # Prepare data structures
                    product_service['features'] = [feature.strip() for feature in product_service['features'].split(",")]
                    product_service['benefits'] = [benefit.strip() for benefit in product_service['benefits'].split(",")]

                    crew_outputs = loop.run_until_complete(
                        start_crew_process(
                            business_info,
                            product_service,
                            price,
                            currency,
                            payment_frequency,
                            selling_scope,
                            location,
                            icp_info
                        )
                    )

                    (
                        market_research_output,
                        data_analysis_output,
                        persona_development_output,
                        strategy_recommendations_output,
                        final_report_output
                    ) = crew_outputs

                    record_id = loop.run_until_complete(
                        send_to_airtable(
                            business_info['email'],
                            market_research_output,
                            data_analysis_output,
                            persona_development_output,
                            strategy_recommendations_output,
                            final_report_output
                        )
                    )

                    if record_id:
                        st.success("Data successfully sent to Airtable!")
                        email_sent = send_email(
                            business_info['email'],
                            market_research_output,
                            data_analysis_output,
                            persona_development_output,
                            strategy_recommendations_output,
                            final_report_output
                        )
                        if email_sent:
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
