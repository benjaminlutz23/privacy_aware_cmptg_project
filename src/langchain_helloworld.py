from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

def main():
    print("Initializing ChatOpenAI (LangChain Hello World Test)")
    
    # Initialize the ChatOpenAI model
    try:
        chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        
        # Simple system prompt
        system_message = SystemMessage(content="You are a helpful AI assistant named LangChain Assistant.")
        
        print("ChatOpenAI initialized successfully! You can start chatting (type 'exit' to quit).")
        
        # Simple chat loop
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
                
            # Create a message with the user's input
            human_message = HumanMessage(content=user_input)
            
            # Get response from the model
            response = chat.invoke([system_message, human_message])
            
            print(f"\nLangChain Assistant: {response.content}")
            
    except Exception as e:
        print(f"Error initializing or using ChatOpenAI: {str(e)}")
        print("Check your API key and internet connection.")

if __name__ == "__main__":
    main()
