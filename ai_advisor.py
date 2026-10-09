import sqlite3, requests, os


def ai_advice(client_data):
    """
    The ai_advice function puts forward a couple of considerably reasonable recommendations based off of the client's latest financial status and portfolio.
    """
    my_conn = sqlite3.connect("moneypal_db.db")
    my_cur = my_conn.cursor()

    # Check if we have any clients or not
    my_cur.execute("""SELECT * FROM Clients;""")
    check = my_cur.fetchall()
    if not check:
        print("No clients available!")
        return

    my_conn.commit()
    my_conn.close()

    api_key = os.getenv("MP_API_KEY")

    url = "https://api.avalai.ir/v1/chat/completions"

    prompt = f"""
    You are the AI Financial Advisor for MoneyPal.

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

    Do not make unsupported assumptions about information that isn't provided. The amounts provided are all in dollars!
    """

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    data = {
        "model": "deepseek-flash",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(url, headers=headers, json=data)

    result = response.json()
    answer = result["choices"][0]["message"]["content"]

    print("")
    print("Let's see what our adroitly trained AI Model is going to walk you through --->>>")
    print("")
    print(answer)
