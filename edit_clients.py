import sqlite3, progress_bar, hashlib, time
from prompt_toolkit import prompt


def edit_profile():
    """
    The edit_profile function edits and updates an existing client's profile info.
    """
    my_conn = sqlite3.connect("moneypal_db.db")
    my_cur = my_conn.cursor()

    # Check if we have any clients or not
    my_cur.execute("""SELECT clientID FROM Clients;""")
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
        hashed_password = hashlib.sha256(pass_validation.encode("utf-8")).hexdigest()
        my_cur.execute(
            """SELECT clientID, password
                            FROM Clients
                            WHERE clientID = ? AND password = ?;
            """,
            (
                id_choice,
                hashed_password,
            ),
        )
        client_pass = my_cur.fetchall()
        if not client_pass:
            print("No such client found!")
            return
        else:
            break

    ## UPDATE profile
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
            print("No matches, Try again!")
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
            print(f"Not included, Try again! | {e}")
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

    notes = input("10) Feel free to add any important pieces of notes in here: ")

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

    time.sleep(0.5)
    progress_bar.track_progress()
    print(f"New changes applied successfully to clientID {id_choice}!")
    time.sleep(0.5)

    my_conn.commit()
    my_conn.close()
