import sqlite3, math, time, os
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
            id_choice = int(input("Enter the clientID which you wish to View: "))
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


def view_all():
    """
    The view_all function gives access to all clients' information through the MasterID, besides overall clients' status.
    """
    my_conn = sqlite3.connect("moneypal_db.db")
    my_cur = my_conn.cursor()

    # Check if we have any clients or not
    my_cur.execute("""SELECT * FROM Clients;""")
    check = my_cur.fetchall()
    if not check:
        print("No clients available!")
        return

    # MasterID validation
    master_id = prompt("Enter your MasterID: ", is_password=True)
    if master_id == os.getenv("MP_MASTER_ID"):
        my_cur.execute("""SELECT *
                        FROM Clients;
        """)
        clients = my_cur.fetchall()
        # Display all
        print(
            "=============================================================================="
        )
        for i, info in enumerate(clients, start=1):
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
                f"Client_{i}\n\n"
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
            print(
                "=============================================================================="
            )
            time.sleep(1)

        # Clients Overall Data
        my_cur.execute(
            """SELECT AVG(age), AVG(incomes), AVG(expenses), AVG(assetsAmount), AVG(debtsAmount), AVG(balance)
                        FROM Clients;
        """
        )
        status = my_cur.fetchall()
        print("Clients Overall Data\n")
        print(
            f"AVERAGE...\n"
            f"Age: {math.ceil(status[0][0])}\n"
            f"Incomes: {round(status[0][1], 2)}\n"
            f"Expenses: {round(status[0][2], 2)}\n"
            f"Assets: {round(status[0][3], 2)}\n"
            f"Debts: {round(status[0][4], 2)}\n"
            f"Balance: {round(status[0][5], 2)}"
        )
    else:
        print("Access denied, Try again!")

    my_conn.commit()
    my_conn.close()
