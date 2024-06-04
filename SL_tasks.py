from crewai import Task

# Define the tasks as per the required template
icp_task = Task(
    description=f"""Your task is to create a detailed 400 words ideal customer profile that will guide marketing and product development strategies for a business selling the product ."
            "To generate the ICP, consider the following:"
            "- Analyze the provided customer feedback, market research, and industry reports to identify patterns and insights about the target customer"
            "- Determine the demographic, geographic, and psychographic characteristics of the ideal customer"
            "- Identify the customer's pain points, needs, and challenges related to the product or service"
            "- Describe the customer's goals, desires, and aspirations that the product or service can help fulfill"
            "- Summarize the customer's preferred communication channels and media consumption habits"
            "- List the customer's most common objections and hesitations when considering a purchase of the product or service"
            "- Explore the factors that influence the customer's decision-making process when choosing a product or service in the relevant category"
            "- Create a memorable and relatable name for the ICP that reflects the target customer's characteristics or role (e.g., "Marketing Manager Molly," "Fitness Enthusiast Frank")"
            "If the majority of the target customers are men, use a male example in the profile. If the majority are women, use a female example."
            "The ICP should be written in a professional, analytical tone, with clarity and accessibility necessary for understanding by team members across different functions."
            "Remember to regularly review and update the ICP based on new customer data, market trends, and product changes.""",
        expected_output=f"""Create an ideal customer profile document of approximately 400 words , including:
            "a story-like format that is easy to understand and remember. For example:
            "Meet [Name], a [age]-year-old [gender] who works as a [occupation] in [location]. [Name] values [values] and enjoys [interests/hobbies] in their free time. As a [personality trait] person, [Name] struggles with [pain point/challenge] when it comes to [product/service category]. They aspire to [goal/desire] and believe that the right [product/service] can help them achieve this. [Name] prefers to communicate via [preferred channels] and often consumes media through [media habits]. When considering a purchase, [Name] typically [decision-making process description] and their main concerns are [objections/hesitations]."
            "- A title featuring the memorable ICP name"
            "- A detailed description of the target customer, including:"
            "- Demographic characteristics (e.g., age, gender, income, education, occupation)"
            "- Geographic characteristics (e.g., location, urban/rural, climate)"
            "- Psychographic characteristics (e.g., personality, values, interests, lifestyle)"
            "- A list of the customer's pain points, needs, challenges and jobs to be done some related to the product or service and some outside the scope of our offering but are still important to the customer 4-6 of each."
            "- A description of the customer's goals, desires, and aspirations that the product or service can help fulfill"
            "- A summary of the customer's preferred communication channels (e.g., email, social media, phone) and media consumption habits (e.g., blogs, podcasts, magazines)"
            "- A list of the customer's most common objections and hesitations when considering a purchase of the product or service"
            "- A description of the customer's typical decision-making process, including the steps they take, the information they seek, and the criteria they use to evaluate options"
            "Format the document as a concise, structured report with headings, subheadings, and bullet points for easy reference and sharing among team members."
            "Conclude the ICP with of how the key characteristics can inform marketing and product development strategies."
            "Emphasize the importance of continuously refining the ICP based on new customer data, market trends, and product changes, and suggest a timeline for periodic reviews (e.g., quarterly or bi-annually)."
            "If insufficient information is provided about the target customer or product/service, make reasonable assumptions or provide generic examples, while clearly stating the limitations.""",
    )


jtbd_task = Task(
    description="Job To Be Done analysis for the product.",
    expected_output=""" Create a Jobs to Be Done (JTBD) report based on the simulated interview with the ideal customer profile. The report should be approximately 200 words and include:
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
    description=f"""Your task is to conduct a simulated interview with an ideal customer profile on behalf of a business selling a specific product or service, in order to identify their Jobs to Be Done (JTBD) and explore competing solutions.
            "To generate the simulated interview and JTBD report, consider the following:"
            "- Analyze the provided ideal customer profile to understand their characteristics, goals, and decision-making process"
            "- Develop a set of open-ended questions that will help uncover the customer's JTBD related to the product or service category"
            "- Explore the ways customers are currently solving their problems and what alternatives they consider"
            "- Identify the factors that determine the customer's decision when choosing a solution"
            "- Examine the customer's experience with current solutions and alternatives, including their satisfaction levels, perceived benefits, and limitations"
            "- Prioritize the identified JTBD based on their importance and impact on the customer's decision-making process"
            "- Simulate the customer's responses based on your understanding of their profile and the market"
            "- Synthesize the findings into a clear and concise report that highlights the key JTBD and actionable recommendations"
            "The simulated interview and report should be written in a professional, analytical tone, ensuring clarity and accessibility necessary for understanding by team members across different functions.""",
        expected_output=f"""Create a Jobs to Be Done (JTBD) report based on the simulated interview with the ideal customer profile. The report should be approximately 1000 words in markdown and include:
            "- A title"
            "- An explanation of what JTBD are and why it is essential to identify them"
            "- At least 8 JTBD identified through the simulated interview, each described in detail, 4-5 of these should be related to the product or service and the rest can be outside the scope of the offering but are still important to the customer"
            "- A prioritized list of the identified JTBD based on their importance and impact on the customer's decision-making process, including the reasoning behind the prioritization"
            "- An exploration of the ways customers are currently solving their problems and what alternatives they consider"
            "- An examination of the customer's experience with current solutions and alternatives, including their satisfaction levels, perceived benefits, and limitations"
            "- A discussion of the factors that determine the customer's decision when choosing a solution"
            "- Relevant quotes or examples from the simulated interview to support the findings"
            "Organize the report into the following sections:"
            "1. Introduction to Jobs to Be Done"
            "2. Identified Jobs to Be Done"
            "- JTBD 1"
            "- JTBD 2"
            "- JTBD 3"
            "- JTBD 4"
            "- JTBD 5"
            "3. Prioritized Jobs to Be Done"
            "4. Current Solutions and Alternatives"
            "5. Experience with Competing Solutions"
            "6. Decision-Making Factors"
            "7. Key Takeaways and Actionable Recommendations"
            "Use headings, subheadings, bullet points, and numbered lists to structure the report in an easy-to-read format."
            "Explain how gathering this information through interviews helps businesses:"
            "- Refine their product offering"
            "- Target the right audience"
            "- Adjust their marketing and development strategies to better achieve product-market fit"
            "- Engage in a process of continuous learning and iteration, using customer feedback to make informed decisions"
            "Conclude the report with a summary of the key findings and specific, actionable recommendations for the business based on the identified JTBD and customer insights."
            "Use a professional, analytical tone throughout the report, ensuring clarity and accessibility necessary for understanding by team members across different functions."
            "If insufficient information is provided about the ideal customer profile or product/service, make reasonable assumptions or provide generic examples, while clearly stating the limitations.""",
    )
