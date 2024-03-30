from uuid import UUID

from starlette import status
from starlette.exceptions import HTTPException

from src.client.cockroach import CockroachDBClient
from src.db.service import DBservice
from src.db.table.asset import Asset
from src.db.table.bank import Bank
from src.db.table.credit_card import CreditCard
from src.db.table.emi import EMI
from src.db.table.fd import FD
from src.db.table.loan import Loan
from src.db.table.stock import Stock
from src.db.table.transaction import Transaction
from src.db.table.user import User
from src.schemas.investment import AssetResponse, FDResponse, StockResponse
from src.schemas.liability import EMIResponse, LoanResponse
from src.schemas.user import TransactionResponse
from src.schemas.wallet import BankResponse, CreditCardResponse
from src.utils.enums import HolderType


class GetService:
    @classmethod
    def evaluateTransaction(cls, transaction: Transaction) -> TransactionResponse:
        transaction_type = ""
        if transaction.from_account_type == HolderType.income:
            transaction_type = "Income"
        elif transaction.to_account_type == HolderType.expense:
            transaction_type = "Expense"
        elif transaction.to_account_type == HolderType.emi:
            transaction_type = "EMI Payment"
        elif transaction.to_account_type == HolderType.loan:
            transaction_type = "Loan Payment"
        elif transaction.to_account_type == HolderType.stock:
            transaction_type = "Stock Purchase"
        elif transaction.to_account_type == HolderType.credit_card:
            transaction_type = "Credit Card Payment"
        elif transaction.to_account_type == HolderType.fd:
            transaction_type = "FD Purchase"
        elif transaction.to_account_type == HolderType.asset:
            transaction_type = "Asset Purchase"
        elif transaction.from_account_type == HolderType.loan:
            transaction_type = "Loan Disbursement"
        elif transaction.from_account_type == HolderType.emi:
            transaction_type = "EMI Disbursement"
        elif transaction.from_account_type == HolderType.stock:
            transaction_type = "Stock Sale"
        elif transaction.from_account_type == HolderType.fd:
            transaction_type = "FD Break"
        elif transaction.from_account_type == HolderType.asset:
            transaction_type = "Asset Sale"
        return TransactionResponse(
            id=transaction.id,
            created_at=transaction.created_at,
            amount=transaction.amount,
            remarks=transaction.remarks,
            transaction_type=transaction_type,
            from_id=transaction.from_account_id,
            from_type=transaction.from_account_type,
            to_id=transaction.to_account_id,
            to_type=transaction.to_account_type,
        )

    @classmethod
    def get_transactions(
        cls, user: User, cockroach_client: CockroachDBClient
    ) -> list[TransactionResponse]:
        transactions: list[Transaction] = cockroach_client.query(
            Transaction.get_by_field_multiple,
            field="user_id",
            match_value=user.id,
            error_not_exist=False,
        )
        if transactions is None:
            return []
        return [cls.evaluateTransaction(transaction) for transaction in transactions]

    @classmethod
    def get_banks(
        cls, user: User, cockroach_client: CockroachDBClient
    ) -> list[BankResponse]:
        banks: list[Bank] = cockroach_client.query(
            Bank.get_by_field_multiple,
            field="user_id",
            match_value=user.id,
            error_not_exist=False,
        )
        if banks is None:
            return []
        return [
            BankResponse(
                id=bank.id,
                name=bank.name,
                bank_name=bank.bank_name,
                balance=bank.balance,
                created_at=bank.created_at,
                disabled=bank.disabled,
                remarks=bank.remarks,
            )
            for bank in banks
        ]

    @classmethod
    def get_cards(
        cls, user: User, cockroach_client: CockroachDBClient
    ) -> list[CreditCardResponse]:
        cards: list[CreditCard] = cockroach_client.query(
            CreditCard.get_by_field_multiple,
            field="user_id",
            match_value=user.id,
            error_not_exist=False,
        )
        if cards is None:
            return []
        return [
            CreditCardResponse(
                id=card.id,
                created_at=card.created_at,
                name=card.name,
                card_name=card.card_name,
                card_limit=card.credit_limit,
                pending_limit=card.credit_limit - card.pending,
                balance=card.pending,
                disabled=card.disabled,
                remarks=card.remarks,
            )
            for card in cards
        ]

    @classmethod
    def get_loans(
        cls, user: User, cockroach_client: CockroachDBClient
    ) -> list[LoanResponse]:
        loans: list[Loan] = cockroach_client.query(
            Loan.get_by_field_multiple,
            field="user_id",
            match_value=user.id,
            error_not_exist=False,
        )
        if loans is None:
            return []
        return [
            LoanResponse(
                id=loan.id,
                created_at=loan.created_at,
                name=loan.name,
                bank_name=loan.bank_name,
                paid=loan.total_amount - loan.pending,
                total_amount=loan.total_amount,
                disabled=loan.disabled,
                remarks=loan.remarks,
            )
            for loan in loans
        ]

    @classmethod
    def get_emis(
        cls, user: User, cockroach_client: CockroachDBClient
    ) -> list[EMIResponse]:
        emis: list[EMI] = cockroach_client.query(
            EMI.get_by_field_multiple,
            field="user_id",
            match_value=user.id,
            error_not_exist=False,
        )
        if emis is None:
            return []
        return [
            EMIResponse(
                id=emi.id,
                created_at=emi.created_at,
                name=emi.name,
                bank_name=emi.bank_name,
                monthly=emi.monthly,
                pending=emi.pending,
                total_time=emi.total_time,
                disabled=emi.disabled,
                remarks=emi.remarks,
            )
            for emi in emis
        ]

    @classmethod
    def get_fds(
        cls, user: User, cockroach_client: CockroachDBClient
    ) -> list[FDResponse]:
        fds: list[FD] = cockroach_client.query(
            FD.get_by_field_multiple,
            field="user_id",
            match_value=user.id,
            error_not_exist=False,
        )
        if fds is None:
            return []
        return [
            FDResponse(
                id=fd.id,
                created_at=fd.created_at,
                bank_name=fd.bank_name,
                initial_amount=fd.amount,
                interest_rate=fd.interest_rate,
                duration=fd.duration,
                sell_amount=fd.sell_amount,
                remarks=fd.remarks,
                disabled=fd.disabled,
            )
            for fd in fds
        ]

    @classmethod
    def get_stocks(
        cls, user: User, cockroach_client: CockroachDBClient
    ) -> list[StockResponse]:
        stocks: list[Stock] = cockroach_client.query(
            Stock.get_by_field_multiple,
            field="user_id",
            match_value=user.id,
            error_not_exist=False,
        )
        if stocks is None:
            return []
        return [
            StockResponse(
                id=stock.id,
                created_at=stock.created_at,
                symbol=stock.symbol,
                quantity_left=stock.amount - stock.already_sold,
                quantity_sold=stock.already_sold,
                remarks=stock.remarks,
                disabled=stock.disabled,
            )
            for stock in stocks
        ]

    @classmethod
    def get_assets(
        cls, user: User, cockroach_client: CockroachDBClient
    ) -> list[AssetResponse]:
        assets: list[Asset] = cockroach_client.query(
            Asset.get_by_field_multiple,
            field="user_id",
            match_value=user.id,
            error_not_exist=False,
        )
        if assets is None:
            return []
        return [
            AssetResponse(
                id=asset.id,
                created_at=asset.created_at,
                name=asset.name,
                initial_amount=asset.amount,
                sell_price=asset.sell_price,
                remarks=asset.remarks,
                disabled=asset.disabled,
            )
            for asset in assets
        ]

    @classmethod
    def get_bank(
        cls, id: UUID, user: User, cockroach_client: CockroachDBClient
    ) -> BankResponse:
        bank: Bank = cockroach_client.query(
            Bank.get_by_multiple_field_unique,
            fields=["id", "user_id"],
            match_values=[id, user.id],
            error_not_exist=False,
        )
        if bank is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bank not found",
            )
        transactions: list[Transaction] = cockroach_client.query(
            DBservice.get_transactions,
            id=bank.id,
        )
        return BankResponse(
            id=bank.id,
            name=bank.name,
            bank_name=bank.bank_name,
            balance=bank.balance,
            created_at=bank.created_at,
            disabled=bank.disabled,
            remarks=bank.remarks,
            transactions=[
                cls.evaluateTransaction(transaction) for transaction in transactions
            ],
        )

    @classmethod
    def get_card(
        cls, id: UUID, user: User, cockroach_client: CockroachDBClient
    ) -> CreditCardResponse:
        card: CreditCard = cockroach_client.query(
            CreditCard.get_by_multiple_field_unique,
            fields=["id", "user_id"],
            match_values=[id, user.id],
            error_not_exist=False,
        )
        if card is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card not found",
            )
        transactions: list[Transaction] = cockroach_client.query(
            DBservice.get_transactions,
            id=card.id,
        )
        return CreditCardResponse(
            id=card.id,
            created_at=card.created_at,
            name=card.name,
            card_name=card.card_name,
            card_limit=card.credit_limit,
            pending_limit=card.credit_limit - card.pending,
            balance=card.pending,
            disabled=card.disabled,
            remarks=card.remarks,
            transactions=[
                cls.evaluateTransaction(transaction) for transaction in transactions
            ],
        )

    @classmethod
    def get_emi(
        cls, id: UUID, user: User, cockroach_client: CockroachDBClient
    ) -> EMIResponse:
        emi: EMI = cockroach_client.query(
            EMI.get_by_multiple_field_unique,
            fields=["id", "user_id"],
            match_values=[id, user.id],
            error_not_exist=False,
        )
        if emi is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="EMI not found",
            )
        transactions: list[Transaction] = cockroach_client.query(
            DBservice.get_transactions,
            id=emi.id,
        )
        return EMIResponse(
            id=emi.id,
            created_at=emi.created_at,
            name=emi.name,
            bank_name=emi.bank_name,
            monthly=emi.monthly,
            pending=emi.pending,
            total_time=emi.total_time,
            disabled=emi.disabled,
            remarks=emi.remarks,
            transactions=[
                cls.evaluateTransaction(transaction) for transaction in transactions
            ],
        )

    @classmethod
    def get_loan(
        cls, id: UUID, user: User, cockroach_client: CockroachDBClient
    ) -> LoanResponse:
        loan: Loan = cockroach_client.query(
            Loan.get_by_multiple_field_unique,
            fields=["id", "user_id"],
            match_values=[id, user.id],
            error_not_exist=False,
        )
        if loan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found",
            )
        transactions: list[Transaction] = cockroach_client.query(
            DBservice.get_transactions,
            id=loan.id,
        )
        return LoanResponse(
            id=loan.id,
            created_at=loan.created_at,
            name=loan.name,
            bank_name=loan.bank_name,
            paid=loan.total_amount - loan.pending,
            total_amount=loan.total_amount,
            disabled=loan.disabled,
            remarks=loan.remarks,
            transactions=[
                cls.evaluateTransaction(transaction) for transaction in transactions
            ],
        )

    @classmethod
    def get_fd(
        cls, id: UUID, user: User, cockroach_client: CockroachDBClient
    ) -> FDResponse:
        fd: FD = cockroach_client.query(
            FD.get_by_multiple_field_unique,
            fields=["id", "user_id"],
            match_values=[id, user.id],
            error_not_exist=False,
        )
        if fd is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="FD not found",
            )
        transactions: list[Transaction] = cockroach_client.query(
            DBservice.get_transactions,
            id=fd.id,
        )
        return FDResponse(
            id=fd.id,
            created_at=fd.created_at,
            bank_name=fd.bank_name,
            initial_amount=fd.amount,
            interest_rate=fd.interest_rate,
            duration=fd.duration,
            sell_amount=fd.sell_amount,
            remarks=fd.remarks,
            disabled=fd.disabled,
            transactions=[
                cls.evaluateTransaction(transaction) for transaction in transactions
            ],
        )

    @classmethod
    def get_stock(
        cls, id: UUID, user: User, cockroach_client: CockroachDBClient
    ) -> StockResponse:
        stock: Stock = cockroach_client.query(
            Stock.get_by_multiple_field_unique,
            fields=["id", "user_id"],
            match_values=[id, user.id],
            error_not_exist=False,
        )
        if stock is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stock not found",
            )
        transactions: list[Transaction] = cockroach_client.query(
            DBservice.get_transactions,
            id=stock.id,
        )
        return StockResponse(
            id=stock.id,
            created_at=stock.created_at,
            symbol=stock.symbol,
            quantity_left=stock.amount - stock.already_sold,
            quantity_sold=stock.already_sold,
            remarks=stock.remarks,
            disabled=stock.disabled,
            transactions=[
                cls.evaluateTransaction(transaction) for transaction in transactions
            ],
        )

    @classmethod
    def get_asset(
        cls, id: UUID, user: User, cockroach_client: CockroachDBClient
    ) -> AssetResponse:
        asset: Asset = cockroach_client.query(
            Asset.get_by_multiple_field_unique,
            fields=["id", "user_id"],
            match_values=[id, user.id],
            error_not_exist=False,
        )
        if asset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found",
            )
        transactions: list[Transaction] = cockroach_client.query(
            DBservice.get_transactions,
            id=asset.id,
        )
        return AssetResponse(
            id=asset.id,
            created_at=asset.created_at,
            name=asset.name,
            initial_amount=asset.amount,
            sell_price=asset.sell_price,
            remarks=asset.remarks,
            disabled=asset.disabled,
            transactions=[
                cls.evaluateTransaction(transaction) for transaction in transactions
            ],
        )
