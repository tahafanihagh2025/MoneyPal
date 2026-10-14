import time, sqlite3, progress_bar, hashlib
from prompt_toolkit import prompt


def add_client():
    """
    The add_client function receives the client information and makes a record for each.
    """
    my_conn = sqlite3.connect("moneypal_db.db")
    my_cur = my_conn.cursor()

    ## Get the client's info
    first_name = input("1) What's your first name?* ")
    last_name = input("2) What's your last name?* ")

    # inp_age validation
    while True:
        try:
            age = int(input("3) How old are you? "))
        except ValueError as e:
            print(f"Not included, Try again! | {e}")
        else:
            break

    # inp_password validation
    while True:
        password = input(
            "4) Set a strong password* (Could be a combination of numbers, letters and symbols)\nFORMART -> nondigits_digits: "
        )
        password_repeat = prompt("Enter the password again: ", is_password=True)
        if password == password_repeat:
            password = password_repeat
            break
        else:
            print("No matches, Try again!\n")
            continue

    original_password = password
    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    password_set = (original_password, hashed_password)

    # inp_incomes, expenses validation
    while True:
        try:
            incomes = float(input("5) Enter your total incomes amount ($): "))
            expenses = float(input("6) Enter your total expenses amount ($): "))
        except ValueError as e:
            print(f"Not included, Try again! | {e}\n")
        else:
            break

    # inp_assets, debts validation
    while True:
        try:
            assets = float(input("7) Enter your total assets amount ($): "))
            debts = float(input("8) Enter your total debts amount ($): "))
        except ValueError as e:
            print(f"Not included, Try again! | {e}")
        else:
            break

    balance = round((incomes + assets) - (expenses + debts), 2)

    account_type = input("9) What's your account type? ")

    notes = input(
        "10) Feel free to add any important pieces of notes in here (passwords especially): "
    )

    client_info = (
        first_name,
        last_name,
        age,
        password_set[1],
        incomes,
        expenses,
        assets,
        debts,
        balance,
        account_type,
        notes,
    )

    # Insert client's info into the Clients table
    my_cur.execute(
        """INSERT INTO Clients (firstName, lastName, age, password, incomes, expenses, assetsAmount, debtsAmount, balance, accountType, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """,
        client_info,
    )

    time.sleep(0.5)
    progress_bar.track_progress()
    print(
        f"New client {first_name.capitalize()} with an ID number of {my_cur.lastrowid} added successfully!"
    )
    time.sleep(0.5)

    my_conn.commit()
    my_conn.close()
