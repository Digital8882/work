from crewai import Task


# Ensure that icp_task, jtbd_task, and pains_task are defined properly

def icp_task():
    # Your function implementation
    pass

def jtbd_task():
    # Your function implementation
    pass

def pains_task():
    # Your function implementation
    pass

# If these tasks are more complex and use Task classes, ensure they are properly indented
icp_task = Task(
    description=f"Identify customer pains related to {product}.",
    expected_output=f"<h1>200 words.Customer Pains for {product}</h1>",
)

jtbd_task = Task(
    description=f"Identify the Jobs to Be Done (JTBD) for {product}.",
    expected_output=f"<h1>200 words.Jobs to Be Done (JTBD) for {product}</h1>"
)

pains_task = Task(
    description=f"Create a detailed 1400 words ideal customer profile for {product}.",
    expected_output=f"<h1>200 words.Ideal Customer Profile for {product}</h1>"
)
