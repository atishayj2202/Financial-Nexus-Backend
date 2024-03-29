from starlette import status
from starlette.exceptions import HTTPException

from src.client.cockroach import CockroachDBClient
from src.db.service import DBservice
from src.db.table.bank import Bank
from src.db.table.credit_card import CreditCard
from src.db.table.expenses import Expense
from src.db.table.transaction import Transaction
from src.db.table.user import User
from src.schemas.income import CreateTransactionRequest, ExpenseRequest, IncomeRequest
from src.schemas.wallet import CreateBankRequest, CreateCreditCardRequest
from src.utils.enums import HolderType


class AddService:
    @classmethod
    def add_bank(
        cls, request: CreateBankRequest, cockroach_client: CockroachDBClient, user: User
    ):
        if request.opening_balance < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Opening balance cannot be negative",
            )
        bank: Bank = Bank(
            user_id=user.id,
            name=request.name,
            bank_name=request.bank_name,
            balance=request.opening_balance,
            remarks=request.remarks,
        )
        cockroach_client.query(
            Bank.add,
            items=[bank],
        )

    @classmethod
    def add_card(
        cls,
        request: CreateCreditCardRequest,
        cockroach_client: CockroachDBClient,
        user: User,
    ):
        if request.card_limit < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Card limit cannot be negative",
            )
        card: CreditCard = CreditCard(
            user_id=user.id,
            name=request.name,
            card_name=request.card_name,
            remarks=request.remarks,
            credit_limit=request.card_limit,
        )
        cockroach_client.query(
            CreditCard.add,
            items=[card],
        )

    @classmethod
    def add_income(
        cls,
        request: IncomeRequest,
        cockroach_client: CockroachDBClient,
        user: User,
    ):
        if request.amount < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Income amount cannot be negative",
            )
        bank: Bank = cockroach_client.query(
            Bank.get_id,
            id=request.bank_id,
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
                detail="Bank not belong to user",
            )
        cockroach_client.queries(
            fn=[Transaction.add, DBservice.update_bank_balance],
            kwargs=[
                {
                    "items": [
                        Transaction(
                            user_id=user.id,
                            from_account_type=HolderType.income,
                            to_account_id=bank.id,
                            to_account_type=HolderType.bank,
                            amount=request.amount,
                            remarks=request.remarks,
                        )
                    ]
                },
                {"id": bank.id, "amount": request.amount},
            ],
        )

    @classmethod
    def add_expense(
        cls, request: ExpenseRequest, cockroach_client: CockroachDBClient, user: User
    ):
        if request.price < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Expense price cannot be negative",
            )
        expense: Expense = Expense(
            user_id=user.id,
            name=request.name,
            amount=request.price,
            remarks=request.remarks,
        )
        cockroach_client.queries(
            fn=[Expense.add, DBservice.pay_transaction],
            kwargs=[
                {"items": [expense]},
                {
                    "to_account_type": HolderType.expense,
                    "to_account_id": expense.id,
                    "user": User,
                    "cockroach_client": cockroach_client,
                    "request": CreateTransactionRequest(
                        amount=request.amount,
                        remarks=request.remarks,
                        from_account_id=request.from_account_id,
                        from_credit_card_id=request.from_credit_card_id,
                        from_loan=request.from_loan,
                        from_emi=request.from_emi,
                    ),
                },
            ],
        )
