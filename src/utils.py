from typing import List
import schemas

def get_loan_payments_for_loan_terms(
            monthly_interest_rate: float,
            principal_amount: float,
            number_of_terms: int
        ) -> List[schemas.LoanPayment]:
    pass
