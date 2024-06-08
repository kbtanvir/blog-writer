from cleantext import clean
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()


class BlogWriterAgent:
    def __init__(
        self,
        topic,
        length,
        outline="""
                 hook,
                 attention,
                 interest, 
                 desire,
                 action,
                 """
    ):
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
            description=f"Generate a blog post on the topic: '{self.topic}' with a length of {self.length} words following this structure: '{self.outline}' each outline should have a proper title.",
            agent=self.blog_writer,
            expected_output="A well-written blog post that adheres to the provided structure."
        )

        self.edit_blog_post = Task(
            description="Review and edit the generated blog post to ensure it meets the quality standards and structure requirements, make sure there is enough variation of grammar styles to keep articles engaging, prevent repeatiation of titles, add strong tags where applicable in p tag",
            agent=self.blog_editor,
            expected_output="blog artile with proper h1, h2, p tags"
        )
        self.remove_reponses = Task(
            description="remove any response that is not a part of blog article,",
            agent=self.blog_editor,
            expected_output="""
            <h1>title</h1> 
            <h2>some sub heading 1</h2>
            <p></p>
            <h2>some sub heading 2</h2>
            <p></p>
            <h2>additional number of sub headings as needed</h2>
            <p></p>
            """
        )

        self.blog_writer_crew = Crew(
            agents=[self.blog_writer, self.blog_editor],
            tasks=[self.generate_blog_post, self.edit_blog_post, self.remove_reponses],
            verbose=2,
            process=Process.sequential
        )

    def generate(self):
        output = self.blog_writer_crew.kickoff()
        return output


class TopicGeneratorAgent:
    def __init__(
        self,
        niche='Digital Marketing',
        count=10,
        outline="""
                 each topic should be a long title,
                 there should be a variation of topics containing viral elements such as
                    1. Contradictory Curiosity...
                    2. Tangible Timeframe ...
                    3. Insider Authority ...
                    4. Using Negativity ...
                    5. Weight of Regret ...
                    6. Personal Victory ...
                    7. Cliffhanger Question ...
                    8. Broad Relatability,
                 """
    ):
        self.niche = niche
        self.count = count
        self.outline = outline

        self.topic_generator = Agent(
            role="Topic Generator",
            goal="Generate engaging and varied blog topics within the given niche, incorporating the specified viral elements.",
            backstory="You are an AI assistant specialized in brainstorming compelling blog topics to boost content engagement.",
            verbose=True,
            allow_delegation=False
        )

        self.topic_refiner = Agent(
            role="Topic Refiner",
            goal="Ensure the generated topics are clean, removing any number orders or context keywords, and outputting only generated titles in array of text format. ",
            backstory="You are an AI assistant tasked with refining generated blog topics to meet specified formatting guidelines.",
            verbose=True,
            allow_delegation=False
        )

        self.generate_topics = Task(
            description=f"Generate {self.count} blog topics for the niche: '{self.niche}' following this outline: '{self.outline}'",
            agent=self.topic_generator,
            expected_output="A list of engaging and varied blog topics adhering to the provided outline."
        )

        self.refine_topics = Task(
            description="Review and clean the generated topics, removing any number orders or context keywords, remove backslash or forward slashes, remove linebreaks,  each topic,",
            agent=self.topic_refiner,
            expected_output="topic 1 -- topic 2 -- topic 3 -- so on..."
        )
        # self.refine_topics2= Task(
        #     description="remove any unusual characters other than separator in the list",
        #     agent=self.topic_refiner,
        #     expected_output="topic 1 -- topic 2 -- topic 3 -- so on..."
        # )

        self.topic_generator_crew = Crew(
            agents=[self.topic_generator, self.topic_refiner],
            tasks=[self.generate_topics, self.refine_topics],
            verbose=2,
            process=Process.sequential
        )

    def generate(self):
        output = self.topic_generator_crew.kickoff()
        # Assuming the output is a string, convert it to a list (array) of topics
        topics = output.split('--') if isinstance(output, str) else output

        return topics


# agent = TopicGeneratorAgent()

# agent.generate()
