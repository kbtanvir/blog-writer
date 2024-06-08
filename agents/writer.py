
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()


class BlogWriter:
    def __init__(self, topic, length, outline):
        self.topic = topic
        self.length = length
        self.outline = outline

        self.blog_writer = Agent(
            role="Blog Writer",
            goal="Generate a well-structured and engaging blog post based on the given topic, length, and structure.",
            backstory="You are an AI assistant tasked with creating high-quality blog content to help streamline the content creation process.",
            verbose=True,
            allow_delegation=False
        )

        self.blog_editor = Agent(
            role="Blog Editor",
            goal="Review and edit the generated blog post to ensure it meets quality standards and adheres to the given structure.",
            backstory="You are an AI assistant responsible for ensuring the quality of the generated blog content.",
            verbose=True,
            allow_delegation=False
        )

        self.generate_blog_post = Task(
            description=f"Generate a blog post on the topic: '{self.topic}' with a length of {self.length} words following this structure: '{self.outline}'",
            agent=self.blog_writer,
            expected_output="A well-written blog post that adheres to the provided structure."
        )

        self.edit_blog_post = Task(
            description="Review and edit the generated blog post to ensure it meets the quality standards and structure requirements.",
            agent=self.blog_editor,
            expected_output="A polished, proper html tags applied to titles, paragraphs and refined blog post ready for publication."
        )

        self.blog_writer_crew = Crew(
            agents=[self.blog_writer, self.blog_editor],
            tasks=[self.generate_blog_post, self.edit_blog_post],
            verbose=2,
            process=Process.sequential
        )

    def generate(self):
        output = self.blog_writer_crew.kickoff()
        return output


# writer = BlogWriter("Who am i", "How long is it?", "What structure does it have?")

# writer.generate()
