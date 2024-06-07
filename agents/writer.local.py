from crewai import Agent, Task, Crew,Process
from langchain_openai import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = "NA"

# Llama3:8b model
llm = ChatOpenAI(
    model="crewai-llama2",
    base_url="http://localhost:11434/v1"
)

topic = "Why climate is changing fast?"
length = 200

structure = """
[hook line]
[intro paragraph] 
[engagement paragraph] 
[fact1]
[fact2] 
[conclusion]
"""

blog_writer = Agent(
    role="Blog Writer",
    goal="Generate a well-structured and engaging blog post based on the given topic, length, and structure.",
    backstory="You are an AI assistant tasked with creating high-quality blog content to help streamline the content creation process.",
    verbose=True,
    allow_delegation=False,
    llm =llm
)

# Define the Blog Editor Agent
blog_editor = Agent(
    role="Blog Editor",
    goal="Review and edit the generated blog post to ensure it meets quality standards and adheres to the given structure.",
    backstory="You are an AI assistant responsible for ensuring the quality of the generated blog content.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Define the Task: Generate the Blog Post
generate_blog_post = Task(
    description=f"Generate a blog post on the topic: '{topic}' with a length of {length} words following this structure: '{structure}'",
    agent=blog_writer,
    expected_output="A well-written blog post that adheres to the provided structure."
)

# Define the Task: Edit the Blog Post
edit_blog_post = Task(
    description="Review and edit the generated blog post to ensure it meets the quality standards and structure requirements.",
    agent=blog_editor,
    expected_output="A polished and refined blog post ready for publication."
)

# Create the Crew
crew = Crew(
    agents=[blog_writer, blog_editor],
    tasks=[generate_blog_post, edit_blog_post],
    verbose=2,
    process=Process.sequential
)

# Execute the Crew
output = crew.kickoff()
print('result :::::')
print(output)
