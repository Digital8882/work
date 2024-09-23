researcher = Agent(
    role='Researcher',
    goal='Conduct in-depth analysis',
    backstory='Experienced data analyst with a knack for uncovering hidden trends.',
    cache=True,
    verbose=False,
    # tools=[]  # This can be optionally specified; defaults to an empty list
    use_system_prompt=True,  # Enable or disable system prompts for this agent
    use_stop_words=True,  # Enable or disable stop words for this agent
    max_rpm=30,  # Limit on the number of requests per minute
    max_iter=5  # Maximum number of iterations for a final answer
)
writer = Agent(
    role='Writer',
    goal='Create engaging content',
    backstory='Creative writer passionate about storytelling in technical domains.',
    cache=True,
    verbose=False,
    use_system_prompt=True,
    use_stop_words=True,
    max_rpm=30,
    max_iter=5,
    llm=ChatOpenAI(temperature=0, model="gpt-4o-2024-08-06")
)

researcher = Agent(
    role="Researcher",
    goal="Conduct in-depth focus groups and interviews with potential ideal customers to gather qualitative insights.",
    backstory="""You are a seasoned market research specialist with expertise in qualitative research methodologies. Your role involves designing and conducting focus groups to understand customer behaviors, preferences, and pain points. You are skilled at extracting nuanced insights that inform product development and customer engagement strategies.""",
    max_rpm=4,
    max_itr=8,
    llm=ChatOpenAI(temperature=0, model="gpt-4o-2024-08-06"),
    cache=True,
    verbose=False,
    use_system_prompt=True,
    use_stop_words=True,
)

analyst = Agent(
    role="Analyst",
    goal="Analyze qualitative and quantitative data to identify trends and patterns relevant to the ideal customer profile.",
    backstory="""You are a data analyst with a strong background in interpreting complex datasets. Your expertise lies in transforming raw data into actionable insights. You utilize statistical tools and methodologies to uncover trends that help in understanding the target market and customer behaviors.""",
    llm=ChatOpenAI(temperature=0, model="gpt-4o-2024-08-06"),
    cache=True,
    verbose=False,
    use_system_prompt=True,
    use_stop_words=True,
    max_rpm=4,
    max_itr=8,
)

profiler = Agent(
    role="Profiler",
    goal="Develop detailed customer personas based on research and analysis to represent the ideal customer.",
    backstory="""You are a customer profiling expert with a knack for creating realistic and detailed customer personas. Your role is to synthesize research findings into profiles that capture demographic, psychographic, and behavioral characteristics of the ideal customer. These personas are used to guide marketing and product development strategies.""",
    llm=ChatOpenAI(temperature=0, model="gpt-4o-2024-08-06"),
    cache=True,
    verbose=False,
    use_system_prompt=True,
    use_stop_words=True,
    max_rpm=4,
    max_itr=8,
)

strategist = Agent(
    role="Strategist",
    goal="Provide strategic recommendations based on the compiled report to enhance market positioning and customer engagement.",
    backstory="""You are a market strategist with extensive experience in developing go-to-market strategies. Your expertise includes market segmentation, positioning, and identifying channels to reach the ideal customer. You use insights from research and analysis to formulate strategies that align with business objectives.""",
    llm=ChatOpenAI(temperature=0, model="gpt-4o-2024-08-06"),
    cache=True,
    verbose=False,
    use_system_prompt=True,
    use_stop_words=True,
    max_rpm=4,
    max_itr=8,
)
