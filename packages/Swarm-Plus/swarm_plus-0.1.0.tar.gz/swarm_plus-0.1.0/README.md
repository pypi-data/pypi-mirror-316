# Swarm-Plus

<div style="display: flex; justify-content: center;">
    <img src="https://i.postimg.cc/KcsDx767/logo.webp" alt="logo.png" width="400"/>
</div>

## Overview: 
Swarm-Plus is a versatile Python framework developed by Vishnu Durairaj, designed to facilitate the creation of intelligent AI agents equipped with a diverse range of tools and functionalities. This open-source framework simplifies the development of sophisticated AI systems capable of handling various tasks through role-based agents and supports advanced multi-agent orchestration.

## Features

- **Built-in User Interface**: Quickly create AI prototypes with a ready-to-use interf
- **Create AI Agents with Tools**: Easily build AI agents with a diverse set of tools.
- **Role-Based Agents**: Define agents with specific roles and responsibilities to handle different tasks and collaborate effectively.
- **Memory Management**: Efficiently handle conversation history with various memory options:
  - **ConversationBufferMemory**: Retains the entire conversation history. Use this when you need to maintain a complete record of all interactions without any summarization or truncation.
  - **ConversationBufferWindowMemory**: Retains only the last K messages in the conversation. Ideal for scenarios where you want to limit memory usage and only keep the most recent interactions. (`memory = ConversationBufferWindowMemory(last_k=3)`)
  - **ConversationSummaryMemory**: Automatically summarizes the conversation once it exceeds a specified number of messages. Use this to manage lengthy conversations by creating concise summaries while retaining overall context. (`memory = ConversationSummaryMemory(number_of_messages=5)`)
  - **ConversationSummaryBufferMemory**: Combines summarization with selective message retention. Summarizes the conversation after a certain point and retains only the most recent N messages. Perfect for balancing context preservation with memory constraints by keeping key recent interactions while summarizing earlier ones. (`memory = ConversationSummaryBufferMemory(buffer_size=5)`)

##  Flexible Integration: Supported AI Model Providers:
- OpenAI
- Anthropic
- Groq
- Ollama

## Colab Notebook

You can try out the notebook directly in Google Colab using the following link:

<a href="https://colab.research.google.com/drive/1cRVz-YS8Cf_GO-uTo0WUz5pLYTj_l4pn?usp=sharing" style="display: flex; align-items: center; text-decoration: none;">
    <img src="https://colab.research.google.com/img/colab_favicon_256px.png" alt="Open in Google Colab" width="150"/>
</a>


## Installation

You can install the Swarm-Plus framework using pip:

```bash

pip install Swarm-Plus

```

## Example Use Case

### 1. Agents With Tools

Here’s an example of how to create a agent with tools using SwarmPlus:

#### Step 1: Import Required Modules

```python
import os
import nest_asyncio
from SwarmPlus.helper import print_colored
from SwarmPlus.agent import Agent
from SwarmPlus.models import OpenaiChatModel
from SwarmPlus.memory import ConversationBufferMemory
from SwarmPlus.tools.FileOperationsTool import SaveFile, CreateFolder
```

#### Step 2. If you are running this script in a notebook uncomment this

```python
# nest_asyncio.apply()
```

#### Step 3. Prepare Agent Description and Instructions
```python
# This concise description helps in understanding the agent's responsibilities and guides the system 
# in determining what types of tasks should be assigned to this agent. 
description = "Responsible for writing story."

# Provide instructions for the agent (System Prompt)
instruction = "You are a creative storyteller who crafts imaginative narratives with vivid details, rich characters, and unexpected plot twists."
```

#### Step 4: Load pre-defined tools that the agent will use
```python
# These tools enable the agent to create folders and save files
tools = [CreateFolder, SaveFile]
```

#### Step 5: Set your OpenAI API key
```python
openai_api_key = "Your API Key"
# openai_api_key = os.getenv('OPENAI_API_KEY')
```

#### Step 6: Initialize the large language model for the agent
```python
model = OpenaiChatModel(model_name="gpt-4o-mini", api_key=openai_api_key, temperature=0)
```

#### Step 7: Initialize memory - 4 different techniques are available.
```python

memory = ConversationBufferMemory()        
# This option retains the entire conversation history. 
# Use this when you need to maintain a complete record of all interactions without any summarization or truncation.

# memory = ConversationBufferWindowMemory(last_k=3)    
# This option retains only the last K messages in the conversation.
# Ideal for scenarios where you want to limit memory usage and only keep the most recent interactions.

# memory = ConversationSummaryMemory(number_of_messages=5)   
# This option automatically summarizes the conversation once it exceeds a specified number of messages.
# Use this to manage lengthy conversations by creating concise summaries while retaining overall context.

# memory = ConversationSummaryBufferMemory(buffer_size=5)    
# This option combines summarization with selective message retention. It summarizes the conversation after a certain point and retains only the most recent N messages.
# Perfect for balancing context preservation with memory constraints by keeping key recent interactions while summarizing earlier ones.
```

#### Step 8: Initialize the agent with the model, description, instructions, and tools. Set verbose to True to see the steps by step actions.
```python
agent = Agent(model=model, agent_name="AI Assistant", agent_description=description, agent_instructions=instruction, tools=tools, assistant_agents=[],max_allowed_attempts=5, verbose=True,memory=memory)
```

#### Step 9: Start the conversation

```python

print_colored("Starting the application...........", "green")

# Example user input
# user_input = "Create a story about AI agents and save it in a new folder. The story should have two chapters, and each chapter should be saved separately inside the folder"

# ---------------- With UI -------------------------

from SwarmPlus.demo import run_ui_demo

demo = run_ui_demo(agent=agent)

if __name__ == "__main__":

    demo.run()


# ---------------- In Terminal -------------------------

user_input = input("User : ")

# Initialize the messages list to store conversation history
messages = []

# Step 8: Process user input and interact with the agent
while user_input != "bye":
    # The agent processes the user input and generates a response
    output = agent.run(user_input, messages)

    # Update the messages list with the agent's response
    messages = output.messages

    # If verbose=False is set during agent initialization, uncomment the following line to see the agent's responses
    # print_colored(f"Assistant : {output}", "purple")

    # Prompt the user for the next input
    user_input = input("User Input : ")

```

### 2. Creating Custom Tools

Here’s an example of how to create a custom tool using pydantic base model:

```python
import os
from typing import List
from pydantic import BaseModel,Field

class AppendToFile(BaseModel):
    # Based on this docstring, the model will determine when to use this tool. Ensure it clearly describes the tool's purpose.
    """
    Use this tool to append content to an existing file.
    """
    # Provides justification for selecting this tool, helping to ensure it is chosen appropriately and not at random. You can ignore this.
    reasoning :List[str] = Field(description="Why you are using this tool")

    # Thses are the required argument with its data types clearly declared.
    file_name: str = Field(..., description="File name to append to.") 
    content: str = Field(..., description="Content to append.")

    class Config:
        extra = "allow" # By defaule the dontext variable will be passed to each and every tools.

    # Every tool must include a `run` method. This method will be called dynamically during interactions to perform the tool's primary function.
    def run(self):

        # self.context_variables.update({"Name": "Vishnu"}) # You can update the context variable and return it

        try:
            with open(self.file_name, "a") as file:
                file.write(self.content)
            return f"Content appended to file: {self.file_name}",self.context_variables
        except Exception as e:
            return f"An error occurred while appending to the file: {str(e)}",self.context_variables
    
AppendToFile(reasoning=["Thoughts"],file_name="path to the file",content="content to append").run()

```
### 3. Multi-Agents

Here’s an example of how to create multiple agents with tools using SwarmPlus:

```python

import nest_asyncio
from SwarmPlus.agent import Agent
from SwarmPlus.demo import run_ui_demo
from SwarmPlus.models import OpenaiChatModel
from SwarmPlus.memory import ConversationBufferMemory
from SwarmPlus.tools.FileOperationsTool import SaveFile, CreateFolder

nest_asyncio.apply()

# Define OpenAI API key

openai_api_key = "OPENAI_API_KEY"

# Shared tools for file and folder operations
tools = [CreateFolder, SaveFile]

# Memory setup for agents
memory = ConversationBufferMemory()

# Step 1: Define the HR Agent
hr_description = "Responsible for handling HR operations, including manpower and staffing queries."
hr_instruction = """
You are the HR manager. Handle all queries related to manpower, hiring, and employee relations. 
Here are some current HR details you can reference:
- Total Employees: 150
- Current Open Positions: 5 (Software Engineer, Data Analyst, HR Specialist, Marketing Coordinator, and Sales Executive)
- Employee Satisfaction Rating: 4.2/5
- Average Tenure: 3 years
- Recent Hires: John Doe (Software Engineer), Sarah Lee (Data Analyst)
- Current Hiring Goals: 3 additional hires for the Sales team, 2 for the Customer Support team
- Upcoming Initiatives: Employee wellness program, leadership training sessions for middle management

Feel free to provide this information in response to queries from the CEO.
"""

hr_model = OpenaiChatModel(model_name="gpt-4o-mini", api_key=openai_api_key, temperature=0)
hr_agent = Agent(
    model=hr_model,
    agent_name="HR Agent",
    agent_description=hr_description,
    agent_instructions=hr_instruction,
    tools=tools,
    assistant_agents=[],  # This agent doesn't interact with others in this setup
    max_allowed_attempts=50,
    verbose=True,
    memory=ConversationBufferMemory(),  # Separate memory for HR
)

# Step 2: Define the Sales Agent
sales_description = "Handles all queries and tasks related to sales, including revenue targets and client relations."
sales_instruction = """
You are the Sales manager. Handle all queries related to sales performance, targets, and client relations.
Here are some current Sales details you can reference:
- Monthly Sales Target: $500,000
- Current Month-to-Date Sales: $320,000
- Top Clients: Acme Corp, Globex Industries, Initech, Umbrella Corporation
- Recent Deals Closed: $75,000 with Initech, $45,000 with Globex Industries
- Current Opportunities in Pipeline: 8 (2 in final negotiation, 3 in initial discussions, 3 in proposal review)
- Sales Team Size: 10 members (including 3 senior sales executives, 5 mid-level, 2 junior)
- Quarterly Sales Growth: 8%
- Upcoming Initiatives: New CRM implementation, sales training on advanced negotiation techniques

Feel free to provide this information in response to queries from the CEO.
"""


sales_model = OpenaiChatModel(model_name="gpt-4o-mini", api_key=openai_api_key, temperature=0)
sales_agent = Agent(
    model=sales_model,
    agent_name="Sales Agent",
    agent_description=sales_description,
    agent_instructions=sales_instruction,
    tools=tools,
    assistant_agents=[],  # This agent doesn't interact with others in this setup
    max_allowed_attempts=50,
    verbose=True,
    memory=ConversationBufferMemory(),  # Separate memory for Sales
)

# Step 3: Define the CEO Agent
ceo_description = "CEO responsible for overseeing company operations and interacting with HR and Sales for strategic decisions. Also, help the users with their requests through available sources."
ceo_instruction = "You are the CEO of the company. Communicate with HR for manpower and staffing queries and with Sales for sales strategies and metrics."

ceo_model = OpenaiChatModel(model_name="gpt-4o-mini", api_key=openai_api_key, temperature=0)
ceo_agent = Agent(
    model=ceo_model,
    agent_name="CEO Agent",
    agent_description=ceo_description,
    agent_instructions=ceo_instruction,
    tools=tools,
    assistant_agents=[hr_agent,sales_agent],  # HR and Sales will be added below
    max_allowed_attempts=50, # How many attempts the agent can make to answer the user's question
    verbose=True, # If you want to print the COT in terminal set True
    memory=memory, 
)

# Step 5: Run the UI demo with the CEO agent that interacts with HR and Sales agents
demo = run_ui_demo(agent=ceo_agent)

if __name__ == "__main__":
    demo.run()

```

### 4. Async Implementation

Here’s an example of async implementation:

```python
import os,nest_asyncio,asyncio
from SwarmPlus.helper import print_colored
from SwarmPlus.agent import Agent
from SwarmPlus.models import OpenaiChatModel
from SwarmPlus.tools.FileOperationsTool import SaveFile, CreateFolder
from SwarmPlus.memory import ConversationSummaryBufferMemory,ConversationSummaryMemory,ConversationBufferWindowMemory,ConversationBufferMemory

# If you are running this script in a notebook
# nest_asyncio.apply()

# Step 1: This concise description helps in understanding the agent's responsibilities and guides the system 
# in determining what types of tasks should be assigned to this agent. 
description = "Responsible for writing story."

# Step 2: Provide instructions for the agent (System Prompt)
instruction = "You are a creative storyteller who crafts imaginative narratives with vivid details, rich characters, and unexpected plot twists."

# Step 3: Load pre-defined tools that the agent will use
# These tools enable the agent to create folders and save files
tools = [CreateFolder, SaveFile]

# Step 4: Set your OpenAI API key
openai_api_key = "Your API Key"
# openai_api_key = os.getenv('OPENAI_API_KEY')

# Step 5: Initialize the language model for the agent
model = OpenaiChatModel(model_name="gpt-4o-mini", api_key=openai_api_key, temperature=0)

# Step 6: Initialize memory - 4 different techniques are available.

# This option retains the entire conversation history. 
# Use this when you need to maintain a complete record of all interactions without any summarization or truncation.
memory = ConversationBufferMemory()        


# Initialize the agent
agent = Agent(model=model, agent_name="AI Assistant", agent_description=description, agent_instructions=instruction, tools=tools, assistant_agents=[],max_allowed_attempts=50, verbose=True,memory=memory)

if __name__ =="__main__":

    async def main():

        print_colored("Starting the application...........", "green")

        # Example user input
        # user_input = "Create a story about AI agents and save it in a new folder. The story should have two chapters, and each chapter should be saved separately inside the folder"

        user_input = input("User : ")

        # Initialize the messages list to store conversation history
        messages = []

        # Step 8: Process user input and interact with the agent
        while user_input != "bye":

            # The agent processes the user input and generates a response
            output = await agent.arun(user_input, messages)

            # Update the messages list with the agent's response
            messages = output.messages

            # If verbose=False is set during agent initialization, uncomment the following line to see the agent's responses
            # print_colored(f"Assistant : {output}", "purple")

            # Prompt the user for the next input
            user_input = input("User Input : ")

    asyncio.run(main())

```

## For More Tutorials Visit My:

<a href="https://www.youtube.com/@learnwithvichu" style="display: flex; align-items: center; text-decoration: none;">
    <img src="https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white" alt="YouTube Channel" width="150"/>
</a>

## Let's stay Connected:

<a href="https://www.linkedin.com/in/vishnu-d-121650167" style="display: flex; align-items: center; text-decoration: none;">
    <img src="https://img.shields.io/badge/LinkedIn-%230077B5.svg?style=for-the-badge&logo=LinkedIn&logoColor=white" alt="LinkedIn Profile" width="150"/>
</a>


## License
This project is licensed under the MIT License. - see the LICENSE file for details.