from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crew1.tools.custom_tool import SearchTools
import sys
import os
from dotenv import load_dotenv

# Set up environment variables for OpenAI API
os.environ["OPENAI_API_BASE"] = 'https://api.openai.com/v1'
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4'
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

print("Current working directory:", os.getcwd())
print("Python path:", sys.path)
print("SearchTools:", SearchTools)

@CrewBase
class PythonCrew:
    """Python crew setup for priority-based task management"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Agent Definitions
    @agent
    def project__manager(self) -> Agent:
        return Agent(
            config=self.agents_config['project__manager'],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def python_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['python_developer'],
            verbose=True,
            allow_delegation=False,
            tools=[SearchTools.search_python]
        )

    @agent
    def python_documentation_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['python_documentation_specialist'],
            verbose=True,
            allow_delegation=False,
            tools=[SearchTools.search_python]
        )

    @agent
    def python_quality_assurance_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['python_quality_assurance_analyst'],
            verbose=True,
            allow_delegation=False,
            tools=[SearchTools.search_python]
        )

    # Task Definitions
    @task
    def requirements_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['requirements_analysis_task'],
            agent=self.project__manager(),
            output_file="requirements_document.md",
            priority=1  # Highest priority for requirements analysis
        )

    @task
    def python_development_task(self) -> Task:
        return Task(
            config=self.tasks_config['python_development_task'],
            agent=self.python_developer(),
            output_file='app.py',
            priority=2  # Second highest priority after requirements
        )

    @task
    def testing_and_quality_assurance_task(self) -> Task:
        return Task(
            config=self.tasks_config['testing_and_quality_assurance_task'],
            agent=self.python_quality_assurance_analyst(),
            output_file='code_review.md',
            priority=3
        )

    @task
    def documentation_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['documentation_creation_task'],
            agent=self.python_documentation_specialist(),
            output_file='README_Python.md',
            priority=4
        )

    # Crew definition
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.python_developer(), self.python_documentation_specialist(), self.python_quality_assurance_analyst()],
            tasks=[self.requirements_analysis_task(), self.python_development_task(), self.testing_and_quality_assurance_task(), self.documentation_creation_task()],
            process=Process.hierarchical,  #sequential, parallel, hierarchical
            manager_agent=self.project__manager(),  # Project Manager oversees the process
            verbose=True,
            share_crew=True
        )
