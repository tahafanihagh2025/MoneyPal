import time

def track_progress():

    for i in range(60):
        print(">", end = "", flush = True)
        time.sleep(0.03)

    print("")
