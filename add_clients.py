import sqlite3
from prompt_toolkit import prompt


def add_client():
    """
    The add_client function receives the client information and makes a record for each.
    """
    my_conn = sqlite3.connect("moneypal_db.db")
    my_cur = my_conn.cursor()

    ## Get the client's info
    first_name = input("What's your first name?* ")
    last_name = input("What's your last name?* ")

    # inp_age validation
    while True:
        try:
            age = int(input("How old are you? "))
        except ValueError as e:
            print(f"Not included, Try again! | {e}")
        else:
            break

    # inp_password validation
    while True:
        password = input(
            "Set a strong password* (Could be a combination of numbers, letters and symbols)\nFORMART -> nondigits_digits: "
        )
        password_redo = prompt("Enter the password again: ", is_password=True)
        if password == password_redo:
            password = password_redo
            break
        else:
            print("No matches, Try again!")
            continue

    # inp_incomes, expenses validation
    while True:
        try:
            incomes = float(input("Enter your total incomes amount ($): "))
            expenses = float(input("Enter your total expenses amount ($): "))
        except ValueError as e:
            print(f"Not included, Try again! | {e}")
        else:
            break

    # inp_assets, debts validation
    while True:
        try:
            assets = float(input("Enter your total assets amount ($): "))
            debts = float(input("Enter your total debts amount ($): "))
        except ValueError as e:
            print(f"Not included, Try again! | {e}")
        else:
            break

    balance = round((incomes + assets) - (expenses + debts), 2)

    account_type = input("What's your account type? ")

    notes = input(
        "Feel free to add any important pieces of notes in here (passwords especially): "
    )

    client_info = (
        first_name,
        last_name,
        age,
        password,
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

    print(
        f"New client {first_name.capitalize()} with an ID number of {my_cur.lastrowid} added successfully!"
    )

    my_conn.commit()
    my_conn.close()
