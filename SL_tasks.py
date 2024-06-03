from crewai import Task

# Define the tasks as per the required template
icp_task = Task(
    description="Identify customer pains related to the product.",
    expected_output="<h1>200 words. Customer Pains for the product</h1>",
)

jtbd_task = Task(
    description="Job To Be Done analysis for the product.",
    expected_output="<h1>200 words. JTBD analysis for the product</h1>",
)

pains_task = Task(
    description="Identify customer pains.",
    expected_output="<h1>200 words. Customer Pains</h1>",
)
