import sqlite3
from prompt_toolkit import prompt


def edit_profile():
    """
    The edit_profile function edits and updates an existing client's profile info.
    """
    my_conn = sqlite3.connect("moneypal_db.db")
    my_cur = my_conn.cursor()

    # Check if we have any clients or not
    my_cur.execute("""SELECT * FROM Clients;""")
    check = my_cur.fetchall()
    if not check:
        print("No clients available!")
        return

    # inp_id validation
    while True:
        try:
            id_choice = int(input("Enter the clientID which you wish to Edit: "))
        except ValueError as e:
            print(f"Not included, Try again! | {e}")
        else:
            break

    # inp_id and password validation
    while True:
        pass_validation = prompt("Enter the password: ", is_password=True)
        my_cur.execute(
            """SELECT clientID, password
                            FROM Clients
                            WHERE clientID = ? AND password = ?;
            """,
            (
                id_choice,
                pass_validation,
            ),
        )
        client_pass = my_cur.fetchall()
        if len(client_pass) == 0:
            print("No such client found!")
            return
        else:
            break

    ## UPDATE profile
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

    notes = input("Feel free to add any important pieces of notes in here: ")

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

    # Update the clientID's row
    my_cur.execute(
        """
    UPDATE Clients
    SET firstName = ?,
        lastName = ?,
        age = ?,
        password = ?,
        incomes = ?,
        expenses = ?,
        assetsAmount = ?,
        debtsAmount = ?,
        balance = ?,
        accountType = ?,
        notes = ?
    WHERE clientID = ?;
""",
        (
            *client_info,
            id_choice,
        ),
    )

    print(f"New changes applied successfully to clientID {id_choice}!")

    my_conn.commit()
    my_conn.close()
