import sqlite3
from prompt_toolkit import prompt


def view_profile():
    """
    The view_profile function provides the client with their record.
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
            id_choice = int(input("Enter the clientID which you wish to view: "))
        except ValueError as e:
            print(f"Not included, Try again! | {e}")
        else:
            break

    my_cur.execute(
        """SELECT clientID, firstName, lastName
                    FROM Clients
                    WHERE clientID = ?;
    """,
        (id_choice,),
    )
    client = my_cur.fetchall()

    if len(client) == 0:
        print(f"No such client found!")
        return
    else:
        for info in client:
            client_id, first_name, last_name = info
            print(
                f"clientID: {client_id}\n"
                f"Full Name: {first_name.capitalize()} {last_name.capitalize()}"
            )

    # More info access
    my_cur.execute(
        """SELECT * 
                    FROM Clients
                    WHERE clientID = ?;
    """,
        (id_choice,),
    )
    client_more = my_cur.fetchall()

    while True:
        more_choice = input("Would you like to see more? (Y / N): ").lower()

        if more_choice == "y":
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
                for info in client_more:
                    (
                        client_id,
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
                    ) = info
                    print(
                        f"clientID: {client_id}\n"
                        f"Full Name: {first_name.capitalize()} {last_name.capitalize()}\n"
                        f"Age: {age} years old\n"
                        f"Password: {password}\n"
                        f"Incomes: {incomes} $\n"
                        f"Expenses: {expenses} $\n"
                        f"Assets: {assets} $\n"
                        f"Debts: {debts} $\n"
                        f"Balance: {balance} $\n"
                        f"Account Type: {account_type}\n"
                        f"IMPORTANT Notes: {notes}"
                    )
                    return info
                break
        elif more_choice == "n":
            print("All right, back to Home: ")
            break
        else:
            print("Not included, Try again!")
            continue

    my_conn.commit()
    my_conn.close()