import crud
import schemas
import state_changes
import nano
import random
from enum import Enum

class UserActivity:
    status: schemas.State
    state: Enum
    ref: object  # firestore DocumentReference
    uid: str

    def __init__(self):

        # create the firebase auth user
        firebase_user = crud.create_firebase_user()
        crud.import_firebase_users([firebase_user])
        self.status, self.state = crud.initial_user_state()
        self.uid = firebase_user.uid

        # create the user in firestore
        _, self.ref = crud.insert_user(schemas.User(uid=self.uid, status=self.status))

        # create the wallet for the user
        personal_wallet = schemas.Wallet(
            wallet_type=schemas.WalletType.WITHDRAW_OR_DEPOSIT,
            address=nano.get_address(),
            status=crud.initial_wallet_state()
        )

        # add the new wallet to the user
        crud.insert_new_wallet_for_user(personal_wallet, self.ref)

    def tick(self):

        # change the state depending on probability configurations
        next_states = state_changes.state_change_config[self.state]
        for next_state in next_states:
            if random.random() < next_states[next_state]['change_probability']:
                crud.status_update(self.ref, next_state)
                next_states[next_state]['on_change_callback'](self.ref)
                print(f"User: {self.uid}, Old State: {self.state}, New State: {next_state}")
                self.state = next_state
