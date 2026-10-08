import sqlite3
from prompt_toolkit import prompt


def remove_client():
    """
    The remove_client function removes an existing client.
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
            id_choice = int(input("Enter the clientID which you wish to remove: "))
        except ValueError as e:
            print(f"Not included, Try again! | {e}")
        else:
            break

    # inp_password and id check
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
            break
        else:
            # Remove the client
            my_cur.execute(
                """DELETE 
                                FROM Clients
                                WHERE clientID = ?;
                """,
                (id_choice,),
            )

            print(f"Client {id_choice} deleted successfully!")
            break

    my_conn.commit()
    my_conn.close()
