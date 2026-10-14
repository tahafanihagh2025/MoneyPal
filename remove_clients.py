import time, sqlite3, progress_bar, hashlib
from prompt_toolkit import prompt


def remove_client():
    """
    The remove_client function removes an existing client.
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
            id_choice = int(input("Enter the clientID which you wish to Remove: "))
        except ValueError as e:
            print(f"Not included, Try again! | {e}")
        else:
            break

    # inp_password and id check
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

            time.sleep(0.5)
            progress_bar.track_progress()
            print(f"Client {id_choice} removed successfully!")
            time.sleep(0.5)
            break

    my_conn.commit()
    my_conn.close()
