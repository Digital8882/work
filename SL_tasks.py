from crewai import Task

# Define the tasks as per the required template
icp_task = Task(
    description="Identify customer pains related to the product.",
    expected_output="""<h1>Marketing Report: {product}</h1>
<h2>Introduction</h2>
<p>The focus group research findings have revealed several key pain points that customers experience with our electric scooters. These include limited battery life, challenges with charging infrastructure, concerns about portability, and the need for improved safety features.</p>
<h2>Customer Pains</h2>
<p>1. <b>Limited Battery Life:</b> Customers expressed frustration with the short battery life of the scooters, which limits their usage and convenience. Many users reported having to recharge frequently, impacting their overall experience.</p>
<p>2. <b>Challenges with Charging Infrastructure:</b> Participants highlighted difficulties in finding convenient and accessible charging stations, leading to inconvenience and range anxiety. The lack of charging infrastructure in certain areas was a major concern for users.</p>"""
)

jtbd_task = Task(
    description="Job To Be Done analysis for the product.",
    expected_output="""<h1>Marketing Report: {product}</h1>
<h2>Introduction</h2>
<p>Investing in a well-designed and reliable product is crucial for customers seeking value and functionality. The Job To Be Done (JTBD) framework helps identify the specific jobs customers are trying to accomplish with the product and the key challenges they face.</p>
<h2>Customer Needs</h2>
<p>1. <b>Reliability:</b> Customers expect the product to be reliable and consistent in performance, ensuring they can depend on it for their daily needs.</p>
<p>2. <b>Advanced Features:</b> Customers look for products that offer advanced features and capabilities that enhance their experience and provide added value.</p>"""
)

pains_task = Task(
    description="Identify customer pains.",
    expected_output="""<h1>Marketing Report: {product}</h1>
<h2>Introduction</h2>
<p>The analysis of customer pains reveals several critical areas that need attention to improve customer satisfaction and loyalty. Understanding these pain points is essential for addressing them effectively.</p>
<h2>Customer Pain Points</h2>
<p>1. <b>High Cost:</b> Customers find the product to be expensive, which may limit its affordability and accessibility. Exploring options to reduce costs or offer flexible payment plans could help alleviate this issue.</p>
<p>2. <b>Usability Issues:</b> Some customers experience difficulties in using the product, indicating a need for better user interface design and more comprehensive user guides.</p>"""
)
