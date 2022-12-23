from __future__ import annotations
import crud
import schemas
import state_changes
import nano
import random
from enum import Enum
import os
from typing import List

class UserActivity:
    status: schemas.State
    state: Enum
    ref: object  # firestore DocumentReference
    uid: str

    """ function for simulation activity """

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

        # perform other user actions randomly
        actions = state_changes.user_activity_config
        for action in actions:
            if random.random() < actions[action]['probability']:
                actions[action]["on_change_callback"](self.ref)

    """ functions for collecting results of the simulation """

    def get_stats(self):
        state_transitions = crud.get_state_transition_history(self.ref)
        return {
            "user": self.uid,
            "date_created": crud.get_user_created_date(self.ref),
            "date_validated": crud.get_user_validated_date(self.ref),
            "current_status": state_transitions[0],
            "state_transition_history": state_transitions
        }
    
    @staticmethod
    def get_state_data(state_ref):
        node_data = state_ref.get().to_dict()
        return {
            'timestamp': node_data['timestamp'],
            'state': schemas.UserState(node_data['state'])
        }

    @staticmethod
    def get_state_transition_history(current_state: schemas.State) -> List[schemas.State]:
        previous_state = crud.traverse_state(current_state, schemas.UserState)
        history = [UserActivity.get_state_data(current_state),]

        while(previous_state):
            history.append(UserActivity.get_state_data(previous_state))
            current_state = previous_state
            previous_state = crud.traverse_state(current_state, schemas.UserState)

        return history

    @staticmethod
    def find_validation_date(transition_history: List[dict]):
        for node in transition_history:
            if node["state"] == schemas.UserState.ACTIVE:
                return node["timestamp"]
        
        return None

    @staticmethod
    def create_csv():
        header = [
            "user",
            "date created",
            "date validated",
            "current status",
            "state transition history"
        ]

        rows = [header,]

        for user in crud.get_all_users():
            user_data = user.to_dict()
            user_state = crud.get_current_state(user.reference)
            transition_history = UserActivity.get_state_transition_history(user_state)
            transition_history.reverse()
            rows.append([
                user_data["uid"],
                transition_history[0]["timestamp"],
                UserActivity.find_validation_date(transition_history),
                transition_history[-1]["state"],
                " -> ".join([str(state["state"]) for state in transition_history])
            ])
        
        print(rows)