from crewai import Task

# Define the tasks as per the required template
icp_task = Task(
    description="Identify the ideal customer.",
    expected_output="""In Plain text format. Create an ideal customer profile document of approximately 250 words, including:
            - A title featuring the memorable ICP name
            - A detailed description of the target customer, including:
            - Demographic characteristics (e.g., age, gender, income, education, occupation)
            - Geographic characteristics (e.g., location, urban/rural, climate)
            - Psychographic characteristics (e.g., personality, values, interests, lifestyle)
            Format the document as a concise, structured report with headings, subheadings, and bullet points for easy reference and sharing among team members.
            Conclude the ICP with of how the key characteristics can inform marketing and product development strategies."""
)

jtbd_task = Task(
    description="Job To Be Done analysis for the product.",
    expected_output="""In Plain text format. Create a Jobs to Be Done (JTBD) report based on the simulated interview with the ideal customer profile. The report should be approximately 200 words and include:
            - A title
            - An explanation of what JTBD are and why it is essential to identify them
            - At least 8 JTBD identified through the simulated interview, each described in detail, 4-5 of these should be related to the product or service and the rest can be outside the scope of the offering but are still important to the customer
            Format the document as a concise, structured report with headings, subheadings, and bullet points for easy reference and sharing among team members.
            Explain how gathering this information through interviews helps businesses:
            - Refine their product offering
            - Target the right audience
            - Adjust their marketing and development strategies to better achieve product-market fit"""
)

pains_task = Task(
    description="Identify customer pains.",
    expected_output="""In Plain text format. Synthesize findings into a report of approximately 250 words, including:
            - A title
            - An overview of the key pain points experienced by the customers, with a detailed analysis of these issues
            - Specific instances of negative experiences customers have had with competing solutions, including direct quotes from customer feedback or focus group discussions
            - Potential objections to current or proposed offerings based on trends observed in customer feedback and market research
            Pains should be related to the jobs-to-be-done (JTBD)
            Each section should begin with an overview followed by detailed examples. 
            Format the document as a concise, structured report with headings, subheadings, and bullet points for easy reference and sharing among team members.
            <p>Conclude the report with a summary that highlights key findings and implications for strategy."""
)
