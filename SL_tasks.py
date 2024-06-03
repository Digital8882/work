from crewai import Task

# Define the tasks as per the required template
icp_task = Task(
    description="Identify the ideal customer.",
    expected_output="""<h1>Create an ideal customer profile document of approximately 250 words, including:</h1>
            <h2>- A title featuring the memorable ICP name</h2>
            <h2>- A detailed description of the target customer, including:</h2>
            <h2>    - Demographic characteristics (e.g., age, gender, income, education, occupation)</h2>
            <h2>    - Geographic characteristics (e.g., location, urban/rural, climate)</h2>
            <h2>    - Psychographic characteristics (e.g., personality, values, interests, lifestyle)</h2>
            <p>Format the document as a concise, structured report with headings, subheadings, and bullet points for easy reference and sharing among team members.</p>
            <p>Conclude the ICP with of how the key characteristics can inform marketing and product development strategies.</p>"""
)

jtbd_task = Task(
    description="Job To Be Done analysis for the product.",
    expected_output="""<h1>Create a Jobs to Be Done (JTBD) report based on the simulated interview with the ideal customer profile. The report should be approximately 200 words in markdown and include:</h1>
            <h2>- A title</h2>
            <h2>- An explanation of what JTBD are and why it is essential to identify them</h2>
            <h2>- At least 8 JTBD identified through the simulated interview, each described in detail, 4-5 of these should be related to the product or service and the rest can be outside the scope of the offering but are still important to the customer</h2>
            <p>Use headings, subheadings, bullet points, and numbered lists to structure the report in an easy-to-read format.</p>
            <p>Explain how gathering this information through interviews helps businesses:</p>
            <p>- Refine their product offering</p>
            <p>- Target the right audience</p>
            <p>- Adjust their marketing and development strategies to better achieve product-market fit</p>"""
)

pains_task = Task(
    description="Identify customer pains.",
    expected_output="""<h1>Synthesize findings into a report of approximately 250 words, including:</h1>
            <h2>- A title</h2>
            <h2>- An overview of the key pain points experienced by the customers, with a detailed analysis of these issues</h2>
            <h2>- Specific instances of negative experiences customers have had with competing solutions, including direct quotes from customer feedback or focus group discussions</h2>
            <h2>- Potential objections to current or proposed offerings based on trends observed in customer feedback and market research</h2>
            <p>Pains should be related to the jobs-to-be-done (JTBD)</p>
            <p>Each section should begin with an overview followed by detailed examples. Include headings, sub-headings, bullet points, and numbered lists to structure the report in an easy-to-read format.</p>
            <p>Conclude the report with a summary that highlights key findings and implications for strategy.</p>"""
)
