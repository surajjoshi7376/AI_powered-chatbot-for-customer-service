from chatbot import pipeline

if __name__ == "__main__":
    print("\nSupport Chatbot (type 'exit' to quit)\n")

    while True:
        user_q = input("User> ").strip()
        if user_q.lower() in {"exit", "quit"}:
            print("Exiting chatbot")
            break

        out = pipeline(user_q)
        print("\n--- ANSWER ---")
        print(out["final_answer"])
        print("\n" + "=" * 60 + "\n")
