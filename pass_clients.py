import sqlite3, hashlib, re
from prompt_toolkit import prompt


def protect_pass():
    """
    The protect_pass function extracts the passwords set in the demonstrated form and converts them into hased bases.
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
            id_choice = int(input("Enter your clientID to access your Notes: "))
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
            my_cur.execute(
                """SELECT notes
                            FROM Clients
                            WHERE clientID = ?;
            """,
                (id_choice,),
            )
            notes = my_cur.fetchall()

            for note in notes:
                result = re.findall(r"\w{1,}_\d{1,}", note[0])

                if len(result) == 0:
                    print("No matches found!")
                else:
                    print(result)
                    for i in range(len(result)):
                        print(
                            f"Hashed base for {result[i]}:",
                            hashlib.md5(result[i].encode("utf-8")).hexdigest(),
                        )
            break

    my_conn.commit()
    my_conn.close()
