from starlette import status
from starlette.exceptions import HTTPException

from src.client.cockroach import CockroachDBClient
from src.db.service import DBservice
from src.db.table.bank import Bank
from src.db.table.credit_card import CreditCard
from src.db.table.expenses import Expense
from src.db.table.fd import FD
from src.db.table.stock import Stock
from src.db.table.transaction import Transaction
from src.db.table.user import User
from src.schemas.income import CreateTransactionRequest, ExpenseRequest, IncomeRequest, CreateTransferTransactionRequest
from src.schemas.investment import CreateStockInvestementRequest, CreateFDRequest
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
        cockroach_client.query(
            DBservice.get_transaction,
            cockroach_client=cockroach_client,
            request=CreateTransferTransactionRequest(
                amount=request.amount,
                remarks=request.remarks,
                to_account_id=request.to_account_id,
            ),
            user=user,
            from_account_id=None,
            from_account_type=HolderType.income,
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

    @classmethod
    def add_stock(cls, request: CreateStockInvestementRequest, user: User, cockroach_client: CockroachDBClient):
        stock = Stock(
            user_id=user.id,
            symbol=request.symbol,
            amount=request.quantity,
            buy_price=request.amount/request.quantity,
            price=request.price,
            remarks=request.remarks,
        )
        cockroach_client.queries(
            fn=[Stock.add, DBservice.pay_transaction],
            kwargs=[
                {"items": [stock]},
                {
                    "to_account_type": HolderType.stock,
                    "to_account_id": stock.id,
                    "user": User,
                    "cockroach_client": cockroach_client,
                    "request": CreateTransactionRequest(
                        amount=request.amount,
                        remarks=request.remarks,
                        from_account_id=request.from_account_id,
                        from_credit_card_id=None,
                        from_loan=None,
                        from_emi=None,
                    ),
                },
            ]
        )

    @classmethod
    def add_fd(cls, request: CreateFDRequest, user: User, cockroach_client: CockroachDBClient):
        fd : FD = FD(
            user_id=user.id,
            bank_name=request.bank_name,
            amount=request.amount,
            interest_rate=request.interest_rate,
            duration=request.duration,
            remarks=request.remarks,
        )
        cockroach_client.queries(
            fn=[FD.add, DBservice.pay_transaction],
            kwargs=[
                {"items": [fd]},
                {
                    "to_account_type": HolderType.fd,
                    "to_account_id": fd.id,
                    "user": User,
                    "cockroach_client": cockroach_client,
                    "request": CreateTransactionRequest(
                        amount=request.amount,
                        remarks=request.remarks,
                        from_account_id=request.from_account_id,
                        from_credit_card_id=None,
                        from_loan=None,
                        from_emi=None,
                    ),
                },
            ]
        )