import config
from core.orchestrator import run_agent
from langchain_core.messages import HumanMessage, AIMessage

def main():
    """Astra assistant ko run karne ke liye main function."""
    print(f"--- Welcome to {config.PROJECT_NAME} ---")
    print("-" * 20)
    print("Aapka personal AI assistant taiyaar hai. 'exit' likh kar band karein.")
    print("-" * 20)

    # Chat history ko store karne ke liye ek list
    chat_history = []

    while True:
        try:
            user_input = input("Aap > ")
            if user_input.lower() == 'exit':
                print("Astra > Alvida!")
                break

            # Agent ko user input aur purani history dono bhejna
            response_dict = run_agent(user_input, chat_history)
            final_answer = response_dict.get('output', "Sorry, I could not find an answer.")
            print(f"\n>>>> Astra's Final Answer <<<<\n{final_answer}\n")

            # History ko update karna
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=final_answer))

            # Optional: History ko lamba hone se rokna
            if len(chat_history) > 10: # 5 Q&A pairs
                chat_history = chat_history[-10:]


        except KeyboardInterrupt:
            print("\nAstra > Alvida!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()