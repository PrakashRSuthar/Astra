import config
from core.orchestrator import Orchestrator

def main():
    """
    Astra assistant ko run karne ke liye main function.
    """
    print(f"--- Welcome to {config.PROJECT_NAME} ---")
    
    # Orchestrator ka instance banana
    orchestrator = Orchestrator()
    
    print("-" * 20)
    print("Aapka personal AI assistant taiyaar hai. 'exit' likh kar band karein.")
    print("-" * 20)

    while True:
        try:
            user_input = input("Aap > ")

            if user_input.lower() == 'exit':
                print("Astra > Alvida!")
                break
            
            # Input ko seedha Orchestrator ko de rahe hain
            response = orchestrator.run(user_input)
            
            print(f"\n>>>> Astra's Final Answer <<<<\n{response}\n")

        except KeyboardInterrupt:
            print("\nAstra > Alvida!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            

if __name__ == "__main__":
    main()