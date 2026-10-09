import time, os
import create_db, add_clients, remove_clients, view_clients, edit_clients, pass_clients, ai_advisor


print("====================================================")
print("Welcome Back to your state-off-the-art MoneyPal assistant!")
print("====================================================")

# Create table & Initialize it
create_db.create_table()
print("Database initialized successfully!")

inp_choice = "sth"
while inp_choice != "0":
    print("====================================================")
    print(
        "1. Add Client\n2. Remove Client\n3. View Profile\n4. Edit Profile\n5. Passwords Protection\n6. AI Financial Advisor\n7. View All\n0. Exit"
    )
    print("====================================================")

    inp_choice = input("What would you like to do? ")

    os.system("cls")

    if inp_choice == "1":
        time.sleep(0.5)
        add_clients.add_client()

    elif inp_choice == "2":
        time.sleep(0.5)
        remove_clients.remove_client()

    elif inp_choice == "3":
        time.sleep(0.5)
        view_clients.view_profile()

    elif inp_choice == "4":
        time.sleep(0.5)
        edit_clients.edit_profile()

    elif inp_choice == "5":
        time.sleep(0.5)
        pass_clients.protect_pass()

    elif inp_choice == "6":
        time.sleep(0.5)
        client_data = view_clients.view_profile()
        print("")
        ai_choice = input("Enter your AI_Pass: ")

        if ai_choice == os.getenv("MP_MASTER_ID"):
            ai_advisor.ai_advice(client_data)
        else:
            print("Access denied, Try again!")

    elif inp_choice == "7":
        time.sleep(0.5)
        view_clients.view_all()

    elif inp_choice == "0":
        inp_choice = "0"
        print("Goodbye!")
        time.sleep(0.5)

    else:
        print("Not included, Try again!")
        time.sleep(1)
        continue
