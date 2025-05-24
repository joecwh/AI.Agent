from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

# load environmet file
load_dotenv()

# decorator
@tool
def calculator(a: float, b: float) -> str:
    # doc string -> description of the tools
    """Useful for performing basic arithmeric calculations with numbers"""
    return f"the sum of {a} and {b} is {a + b}"

def main():
    # initial open AI
    # temperature = randomness (the higher the random, 0 = accurate)
    model = ChatOpenAI(temperature=0)
    
    tools = [calculator]
    agent_executor = create_react_agent(model, tools)
    
    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me.")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input == 'quit':
            break
        
        # end="" means dont skip line
        print("\nAssistant:", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
                    
        print()
        
# just invoke the main() method
if __name__ == "__main__":
    main()
        
        