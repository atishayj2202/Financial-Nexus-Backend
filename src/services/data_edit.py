from uuid import UUID

from starlette import status
from starlette.exceptions import HTTPException

from src.client.cockroach import CockroachDBClient
from src.db.table.bank import Bank
from src.db.table.credit_card import CreditCard
from src.db.table.emi import EMI
from src.db.table.loan import Loan
from src.db.table.user import User
from src.utils.time import get_current_time


class EditService:
    @classmethod
    def delete_bank(
        cls, bank_id: UUID, user: User, cockroach_client: CockroachDBClient
    ):
        bank: Bank = cockroach_client.query(
            Bank.get_id,
            id=bank_id,
            error_not_exist=False,
        )
        if bank is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bank not found",
            )
        if bank.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
        if bank.disabled is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bank already deleted",
            )
        bank.disabled = get_current_time()
        cockroach_client.query(Bank.update_by_id, new_data=bank, id=bank.id)

    @classmethod
    def delete_card(
        cls, card_id: UUID, user: User, cockroach_client: CockroachDBClient
    ):
        card: CreditCard = cockroach_client.query(
            CreditCard.get_id,
            id=card_id,
            error_not_exist=False,
        )
        if card is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card not found",
            )
        if card.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
        if card.disabled is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Card already deleted",
            )
        card.disabled = get_current_time()
        cockroach_client.query(
            CreditCard.update_by_id,
            new_data=card,
            id=card.id,
        )

    @classmethod
    def close_loan(cls, loan_id: UUID, user: User, cockroach_client: CockroachDBClient):
        loan: Loan = cockroach_client.query(
            Loan.get_id,
            id=loan_id,
            error_not_exist=False,
        )
        if loan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found",
            )
        if loan.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
        if loan.pending > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Loan has pending amount",
            )
        if loan.disabled is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Loan already closed",
            )
        loan.disabled = get_current_time()
        cockroach_client.query(
            Loan.update_by_id,
            new_data=loan,
            id=loan.id,
        )

    @classmethod
    def close_emi(cls, emi_id: UUID, user: User, cockroach_client: CockroachDBClient):
        emi: EMI = cockroach_client.query(
            EMI.get_id,
            id=emi_id,
            error_not_exist=False,
        )
        if emi is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="EMI not found",
            )
        if emi.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
        if emi.disabled is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="EMI already closed",
            )
        if emi.pending > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="EMI has pending amount",
            )
        emi.disabled = get_current_time()
        cockroach_client.query(
            EMI.update_by_id,
            new_data=emi,
            id=emi.id,
        )
