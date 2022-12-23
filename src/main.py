
import user_activity
import threading
import time
import random

users = []

def user_thread():
    user = user_activity.UserActivity()
    users.append(user)
    for i in range(5):
        time.sleep(random.random())
        user.tick()

if __name__ == "__main__":

    count_users = 5

    threads  = []
    # create threads
    for index in range(count_users):
        thread = threading.Thread(target=user_thread, daemon=True)
        threads.append(thread)
        thread.start()

    # join threads
    for index, thread in enumerate(threads):
        thread.join()
    
    # collect data about the run
    user_activity.UserActivity.create_csv()
