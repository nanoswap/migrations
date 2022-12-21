import schemas
import state_change_callbacks

no_op = lambda _: None
state_change_config = {
    schemas.UserState.CREATED: {
        schemas.UserState.VALIDATION_IN_PROGRESS: {"on_change_callback": no_op, "change_probability": 0.25},
    },
    schemas.UserState.VALIDATION_IN_PROGRESS: {
        schemas.UserState.VALIDATION_FAILED: {"on_change_callback": no_op, "change_probability": 0.1},
        schemas.UserState.ACTIVE: {"on_change_callback": state_change_callbacks.validation_succeeded, "change_probability": 0.5},
    },
    schemas.UserState.VALIDATION_FAILED: {
        schemas.UserState.VALIDATION_IN_PROGRESS: {"on_change_callback": no_op, "change_probability": 0.1},
    },
    schemas.UserState.ACTIVE: {
        schemas.UserState.FROZEN: {"on_change_callback": state_change_callbacks.freeze_user_account, "change_probability": 0.1},
    },
    schemas.UserState.FROZEN: {
        schemas.UserState.ACTIVE: {"on_change_callback": state_change_callbacks.unfreeze_user_account, "change_probability": 0.5},
    }
}

user_activity_config = {
    "create_loan": {"on_change_callback": state_change_callbacks.create_loan, "probability": 0.3},
    "stake_loan": {"on_change_callback": state_change_callbacks.stake_loan, "probability": 0.3},
    "withdraw_loan_application": {"on_change_callback": state_change_callbacks.withdraw_loan, "probability": 0.05},
    "deposit_xno": {"on_change_callback": state_change_callbacks.deposit_xno, "probability": 0.2},
    "withdraw_xno": {"on_change_callback": state_change_callbacks.withdraw_xno, "probability": 0.05},
    "transfer_xno": {"on_change_callback": state_change_callbacks.transfer_xno, "probability": 0.1},
    "pay_bill": {"on_change_callback": state_change_callbacks.pay_bill, "probability": 0.1},
    "collect_yield": {"on_change_callback": state_change_callbacks.collect_yield, "probability": 0.1},
}

loan_payment_states = {
    schemas.LoanPaymentState.SCHEDULED: 10,
    schemas.LoanPaymentState.UPCOMING: 10,
    schemas.LoanPaymentState.COMPLETED_ON_TIME: 10,
    schemas.LoanPaymentState.COMPLETED_LATE: 10,
    schemas.LoanPaymentState.LATE: 10,
    schemas.LoanPaymentState.MISSED: 10
}
