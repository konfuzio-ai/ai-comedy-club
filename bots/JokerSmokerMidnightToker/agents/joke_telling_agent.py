from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.chains import LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re
from dotenv import load_dotenv
from tools.CustomOutputParser import CustomOutputParser
from tools.CustomPromptTemplate import CustomPromptTemplate
load_dotenv()

llm=OpenAI(temperature=1)

search = SerpAPIWrapper()
tools = [
    Tool(
        name="Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]

# Set up the base template
template = """Tell me a joke about {input}. You have access to the following tools:

{tools}

Use the following format:

User Input: the topic of the joke
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: write a joke about the topic provided in "User Input"

Begin! 

User Input: {input}
{agent_scratchpad}"""

prompt = CustomPromptTemplate(
    template=template,
    tools=tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps"]
)

llm_chain = LLMChain(llm=llm, prompt=prompt)

tool_names = [tool.name for tool in tools]
agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=CustomOutputParser(),
    stop=["\nObservation:"],
    allowed_tools=tool_names
)

joke_telling_agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

resp = joke_telling_agent_executor.run("tell me a joke about the nation that is the current world cup champion in men's football")
print(resp)

