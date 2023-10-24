from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.chains import LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re
from langchain.memory import ConversationBufferMemory
from bots.JokerSmokerMidnightToker.common.CustomOutputParser import CustomOutputParser
from bots.JokerSmokerMidnightToker.common.CustomPromptTemplate import CustomPromptTemplate


from dotenv import load_dotenv
load_dotenv()

llm=OpenAI(temperature=1)
memory = ConversationBufferMemory(memory_key="chat_history")



search = SerpAPIWrapper()
tools = [
    Tool(
        name="Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]

# Set up the base template
template = """Tell me a joke about {input}, in the context of Chat History below. You have access to the following tools:

{tools}

Use the following format:

User Input: {input}
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: write a joke about the topic provided in "User Input"

Begin! 

Chat History: {chat_history}

User Input: {input}
{agent_scratchpad}"""

prompt = CustomPromptTemplate(
    template=template,
    tools=tools,
    input_variables=["input", "intermediate_steps", "chat_history"]
)

llm_chain = LLMChain(llm=llm, prompt=prompt)

tool_names = [tool.name for tool in tools]
agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=CustomOutputParser(),
    stop=["\nObservation:"],
    allowed_tools=tool_names
)

joke_telling_agent_executor = AgentExecutor.from_agent_and_tools(
  agent=agent, 
  tools=tools, 
  memory=memory,
  verbose=True
)

# reply = joke_telling_agent_executor.run("tell me a monty python joke")
# print(reply)

# second_reply = joke_telling_agent_executor.run("tell me another one")
# print(second_reply)

