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
pains_task = Task(
    description=f"""Simulate focus group discussions based on your expertise and knowledge of the target market. During these sessions, probe deeply to uncover the following:"
            "- Three types of customer pains related to the JTBD (not the product): undesired outcomes, problems, and characteristics (functional, social, emotional, ancillary)"
            "- Pain severity (extreme or moderate)"
            "- Specific expectations for gains and pains"
            "- Barriers and risks related to not getting the job done"
            "- Previous bad experiences with competing solutions"
            "- Potential objections to current or proposed offerings"
            "Explain how understanding customer pain points, bad experiences, and objections helps businesses:"
            "- Prioritize the key pain points to alleviate through improved value propositions"
            "- Identify opportunities for product/service improvement and innovation"
            "- Develop targeted marketing messages that resonate with customers' needs and concerns"
            "- Train customer service teams to address common objections and provide better support"
            "- Inform overall business strategy to better meet customer needs and expectations"
            "This report is intended for internal use by the specified teams to inform strategy and improve customer satisfaction.""",
        expected_output=f"""Synthesize findings into a report of approximately 1200 words, including:  
            "- A title"
            "- An overview of the key pain points experienced by the customers, with a detailed analysis of these issues"
            "- Specific instances of negative experiences customers have had with competing solutions, including direct quotes from customer feedback or focus group discussions"
            "- Potential objections to current or proposed offerings based on trends observed in customer feedback and market research"
            "- Case studies or customer testimonials that exemplify each key pain point, bad experience, and objection, using a format that allows for easy extraction of insights (e.g., bullet points, structured summaries)"
            "Organize the report into three main sections:"
            "1. Customer Pain Points"
            "2. Previous Bad Experiences"
            "3. Possible Objections"
            "Pains should be related to the jobs-to-be-done (JTBD)"
            "Each section should begin with an overview followed by detailed examples. Include headings, sub-headings, bullet points, and numbered lists to structure the report in an easy-to-read format."
            "Conclude the report with a summary that highlights key findings and implications for strategy."
            "Maintain a professional, analytical tone throughout the report, ensuring clarity and accessibility necessary for understanding by team members across different functions."
            "If insufficient information is provided about the business, products/services, or ideal customer profiles, make reasonable assumptions or provide generic examples, while clearly stating the limitations.""",
    )
