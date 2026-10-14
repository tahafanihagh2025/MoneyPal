import sqlite3, os, time, tiktoken
from openai import OpenAI


def ai_advice(client_data):
    """
    The ai_advice function puts forward a couple of considerably reasonable recommendations based off of the client's latest financial status and portfolio.
    """
    my_conn = sqlite3.connect("moneypal_db.db")
    my_cur = my_conn.cursor()

    # Check if we have any clients or not
    my_cur.execute("""SELECT clientID FROM Clients;""")
    check = my_cur.fetchall()
    if not check:
        print("No clients available!")
        return

    my_conn.commit()
    my_conn.close()

    class ChatBot():
        def __init__(self):
            self.llm = OpenAI(
                api_key=os.getenv("MONEYPAL_API_KEY"),
                base_url="https://api.groq.com/openai/v1"
            )
            
            self.prompt = f"""
                Analyze the following client's financial information:
                
                    Name: {client_data[1]}
                    Age: {client_data[3]}
                    Monthly income: {client_data[5]}
                    Monthly expenses: {client_data[6]}
                    Total assets: {client_data[7]}
                    Total debt: {client_data[8]}
                    Current balance: {client_data[9]}
                    Account type: {client_data[10]}
                
                    Provide:
                    1. A brief assessment of the client's financial situation.
                    2. Potential concerns.
                    3. Three practical suggestions.

                    The amounts provided are all in dollars!
                    You're supposed to be succinct, to-the-point and straightforward.
                    Do not make unsupported assumptions about information that isn't provided.
                    
            """
            self.messages = [
                {"role": "system", "content": self.prompt}
            ]

        def bot(self, message):

            self.messages.append({"role": "user", "content": message})

            response = self.llm.chat.completions.create(
                model="qwen/qwen3.8-27b",
                messages = self.messages,
                temperature=0.7,
                # max_tokens=100,
                stream=True
            )

            response_text = ""
            for chunk in response:
                if chunk.choices:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        print(delta, end = '', flush=True)
                        response_text += delta
                        time.sleep(0.05)

            print('')
            self.messages.append({"role": "assistant", "content": response_text})

            return response_text


        def chat(self):
            encoding = tiktoken.get_encoding("cl100k_base")

            while True:
                user_input = input("What's on your mind today? (Enter 'q' to exit!): ").strip().lower()

                if user_input == 'q':
                    print("Goodbye!")
                    break
                else:
                    token_count = len(encoding.encode(user_input))
                    print(f"Token count: {token_count}")

                    if token_count > 25:
                        print(f"You've exceeded the input token count limit, Try again! | {token_count}\n")
                        continue

                    self.bot(user_input)
                    print('')

    print("")
    print("Let's see what our adroitly trained AI Model is going to walk you through --->>>")
    print("")

    def main():
        print("=====================================================================")
        print("Hi there, Welcome to your one and only MoneyPal Financial Advisor!")
        print("=====================================================================")
        bot = ChatBot()
        bot.chat()

    main()
