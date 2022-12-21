from typing import List
import schemas
import state_changes
import crud
import user_activity
import threading
import time
import random

def user_thread():
    user = user_activity.UserActivity()
    for i in range(30):
        time.sleep(random.random())
        user.tick()

if __name__ == "__main__":

    count_users = 10

    threads  = []
    # create threads
    for index in range(count_users):
        thread = threading.Thread(target=user_thread, daemon=True)
        threads.append(thread)
        thread.start()

    # join threads
    for index, thread in enumerate(threads):
        thread.join()
