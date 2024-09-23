from crewai import Task


def task_market_research(business_info, product_service, price, currency, payment_frequency, selling_scope, location, icp_info):
    description = f"""
        Conduct qualitative research to understand the needs, preferences, and pain points of potential customers for the following business:

        - **Business Name:** {business_info['name']}
        - **Business Description:** {business_info['description']}
        - **Unique Value Proposition:** {business_info['unique_value_proposition']}
        - **Product/Service:** {product_service['name']}
          Features: {', '.join(product_service['features'])}
          Benefits: {', '.join(product_service['benefits'])}
        - **Price:** {price} {currency}
        - **Payment Frequency:** {payment_frequency}
        - **Selling Scope:** {selling_scope}
        {"- **Location:** " + location if selling_scope == "Locally" else ""}
        - **Known ICP Information:** {icp_info}

        Prepare a detailed market research analysis addressing the following points:

        1. Identify the primary needs and preferences of the target customers.
        2. Analyze the pain points and challenges they face.
        3. Evaluate how the product/service addresses these needs and pain points.
        4. Provide insights into customer behavior and decision-making processes.

        **Guidelines:**

        - Utilize qualitative data analysis techniques.
        - Reference the provided business and product information.
        - Do not include external data or conduct additional research.
        - Present findings in a clear, structured format.
    """

    def execute():
        response = anthropic_llm.generate(description)
        return response

    return Task(
        description=description,
        expected_output="A comprehensive market research analysis based on the provided business and product information.",
        execute=execute
    )

def task_data_analysis():
    description = """
        Analyze the qualitative data obtained from the market research to identify key trends, patterns, and insights.

        Focus areas include:

        - Common themes in customer feedback.
        - Demographic and psychographic trends.
        - Correlations between customer needs and product features.

        **Guidelines:**

        - Base the analysis solely on the provided market research data.
        - Highlight significant findings with supporting evidence.
        - Use clear and concise language to explain trends and patterns.
    """

    def execute():
        response = openai_llm.generate(description)
        return response

    return Task(
        description=description,
        expected_output="An insightful data analysis report highlighting key trends and patterns from the market research.",
        execute=execute
    )

def task_persona_development():
    description = """
        Develop detailed customer personas based on the data analysis report.

        Each persona should include:

        - **Name and Background**
        - **Demographic Information**
        - **Psychographic Profile**
        - **Goals and Motivations**
        - **Pain Points and Challenges**
        - **Preferred Communication Channels**

        **Guidelines:**

        - Create at least two distinct personas.
        - Ensure personas are realistic and derived from the data.
        - Provide a narrative that brings each persona to life.
    """

    def execute():
        response = openai_llm.generate(description)
        return response

    return Task(
        description=description,
        expected_output="Detailed and realistic customer personas based on the data analysis.",
        execute=execute
    )

def task_strategy_recommendations():
    description = """
        Based on the developed customer personas and insights from previous reports, provide strategic recommendations focusing on:

        - **Customer Engagement Points:** Identify where and how to engage with ideal customers.
        - **Alignment Strategies:** Suggest ways to align the product/service with customer needs and preferences.
        - **Market Positioning:** Offer insights into how to position the product/service in the market effectively.

        **Guidelines:**

        - Do not delve into specific marketing tactics.
        - Focus on strategic, high-level recommendations.
        - Ensure recommendations are actionable and aligned with customer insights.
    """

    def execute():
        response = openai_llm.generate(description)
        return response

    return Task(
        description=description,
        expected_output="Strategic recommendations for engaging with ideal customers and aligning the product/service with their needs.",
        execute=execute
    )

def task_final_report(business_info, product_service, price, currency, payment_frequency, selling_scope, location):
    description = f"""
        Compile all previous analyses and reports into a comprehensive Ideal Customer Profile (ICP) report for **{business_info['name']}**.

        The final report should include:

        1. **Executive Summary**
        2. **Market Research Findings**
        3. **Data Analysis Insights**
        4. **Customer Personas**
        5. **Strategic Recommendations**
        6. **Conclusion**

        **Specific Information to Include:**

        - **Product/Service:** {product_service['name']}
        - **Price:** {price} {currency}
        - **Payment Frequency:** {payment_frequency}
        - **Selling Scope:** {selling_scope}
        {"- **Location:** " + location if selling_scope == "Locally" else ""}

        **Guidelines:**

        - Ensure logical flow and coherence between sections.
        - Use professional language and formatting.
        - The report should be approximately 8 pages in length.
        - Avoid including marketing strategies beyond customer engagement points.
        - Do not add product details beyond what has been provided.
    """

    def execute():
        response = openai_llm.generate(description)
        return response

    return Task(
        description=description,
        expected_output="A comprehensive ICP report ready for presentation.",
        execute=execute
    )
