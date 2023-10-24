from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.chains import LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re
import json
from dotenv import load_dotenv
from bots.JokerSmokerMidnightToker.common.CustomOutputParser import CustomOutputParser
from bots.JokerSmokerMidnightToker.common.CustomPromptTemplate import CustomPromptTemplate
import sys

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
template = """You are an AI joke rating bot. Rate the joke that is provided in the "Joke:" section below. You have access to the following tools:

{tools}

Use the following format:

Final Answer: rate the joke provided in the "Joke:" section. Rating should be between 1 and 10, with 10 being the best joke. 
Provide the answer as JSON output, with the key "rating" and the value being the rating of the joke. Use double-quotes. 
If you have uncertainties about how to rate the joke, just provide a random number between 1 and 10.

Begin! 

Joke: {input}
{agent_scratchpad}"""

prompt = CustomPromptTemplate(
    template=template,
    tools=tools,
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

joke_rating_agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

# resp = joke_rating_agent_executor.run("Why didn't England bring a map to the World Cup? Because they already knew the way to the final!")
# json_resp = json.loads(resp)
# print(json_resp['rating'])

