from crewai import Task

task_market_research = Task(
    description=f"""
        Conduct qualitative research to understand the needs, preferences, and pain points of potential customers for the following business:

        - **Business Description:** {business_info['description']}
        - **Product/Service:** {product_service['name']}
          Features: {', '.join(product_service['features'])}
          Benefits: {', '.join(product_service['benefits'])}
        - **Price:** {price}
        - **Location:** {location}
        - **Unique Value Proposition:** {business_info['unique_value_proposition']}

        Prepare a report summarizing the key findings from focus groups and interviews. The report should cover:

        - Customer pain points and challenges.
        - Customer goals and aspirations.
        - Feedback on the product/service concept.

        **Guidelines:**

        - Do not search the internet; use only the information provided.
        - Present findings in a clear and structured format.
        """,
    expected_output="A market research report summarizing key customer insights.",
    output_file="Market_Research_Report.docx",  # Changed to .docx for simplicity
)

task_data_analysis = Task(
    description="""
        Analyze the data from the market research report to identify trends and patterns. Focus on:

        - Common themes in customer feedback.
        - Demographic trends.
        - Psychographic trends.

        Prepare a data analysis report highlighting these insights.

        **Guidelines:**

        - Use only the data provided from the market research report.
        - Present findings with supporting data and charts where appropriate.
        """,
    expected_output="A data analysis report highlighting trends and patterns.",
    output_file="Data_Analysis_Report.docx",
)

task_persona_development = Task(
    description="""
        Develop detailed customer personas based on the data analysis report. Each persona should include:

        - Name and background.
        - Demographic information.
        - Psychographic profile.
        - Goals and motivations.
        - Pain points and challenges.
        - Preferred communication channels.

        **Guidelines:**

        - Create at least two distinct personas.
        - Ensure personas are realistic and based on the data provided.
        """,
    expected_output="Detailed customer personas in a structured format.",
    output_file="Customer_Personas.docx",
)

task_strategy_recommendations = Task(
    description="""
        Based on the customer personas and insights from previous reports, provide strategic recommendations on:

        - Places where the ideal customers can be found.
        - Engagement strategies (without going into marketing tactics).
        - Suggestions for aligning the product/service with customer needs.

        **Guidelines:**

        - Focus on identifying locations, platforms, or environments where the ideal customer is likely to be present.
        - Do not include marketing strategies or product development details.
        """,
    expected_output="Strategic recommendations focusing on customer engagement points.",
    output_file="Strategic_Recommendations.docx",
)

task_final_report = Task(
    description=f"""
        Compile all the previous reports into a comprehensive Ideal Customer Profile (ICP) report for {business_info['name']}. The final report should include:

        - Executive Summary.
        - Market Research Findings.
        - Data Analysis Insights.
        - Customer Personas.
        - Strategic Recommendations.
        - Conclusion.

        Include the following specific information:
        - Product/Service: {product_service['name']}
        - Price: {price}
        - Location: {location}

        **Guidelines:**

        - Ensure the report flows logically from one section to the next.
        - Use professional language and formatting.
        - The report should be approximately 8 pages long.

        **Important:**

        - Do not include marketing strategies except for places where the ICP can be found.
        - Do not include product details beyond what has been provided.
        """,
    expected_output="A comprehensive ICP report ready for presentation.",
    output_file="ICP_Report.docx",
)
# Establishing the crew with a hierarchical process and additional configurations
