import config
from core.orchestrator import run_agent

def main():
    """Astra assistant ko run karne ke liye main function."""
    print(f"--- Welcome to {config.PROJECT_NAME} ---")
    print("-" * 20)
    print("Aapka personal AI assistant taiyaar hai. 'exit' likh kar band karein.")
    print("-" * 20)
    
    while True:
        try:
            user_input = input("Aap > ")
            if user_input.lower() == 'exit':
                print("Astra > Alvida!")
                break
            
            response_dict = run_agent(user_input)
            
            final_answer = response_dict.get('output', "Sorry, I could not find an answer.")
            print(f"\n>>>> Astra's Final Answer <<<<\n{final_answer}\n")

        except KeyboardInterrupt:
            print("\nAstra > Alvida!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()