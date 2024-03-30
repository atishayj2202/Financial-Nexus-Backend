from uuid import UUID

from sqlalchemy import or_, text
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from src.client.cockroach import CockroachDBClient
from src.db.table.bank import Bank
from src.db.table.credit_card import CreditCard
from src.db.table.emi import EMI
from src.db.table.loan import Loan
from src.db.table.transaction import Transaction
from src.db.table.user import User
from src.schemas.income import (
    CreateTransactionRequest,
    CreateTransferTransactionRequest,
)
from src.utils.enums import HolderType


class DBservice:
    @classmethod
    def get_transactions(cls, db: Session, id: UUID) -> list[Transaction]:
        schema_cls = Transaction._schema_cls()
        result = (
            db.query(schema_cls)
            .filter(
                or_(
                    getattr(schema_cls, "from_account_id") == id,
                    getattr(schema_cls, "to_account_id") == id,
                )
            )
            .all()
        )
        if result:
            return [Transaction.model_validate(r, from_attributes=True) for r in result]
        return []

    @classmethod
    def __verify(cls, user: User, instance):
        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tool not found",
            )
        if instance.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tool not belong to user",
            )
        if instance.disabled is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tool already deleted",
            )

    @classmethod
    def __verify_bank(
        cls, cockroach_client: CockroachDBClient, user: User, bank_id: UUID
    ) -> Bank:
        bank: Bank = cockroach_client.query(
            Bank.get_id,
            id=bank_id,
            error_not_exist=False,
        )
        cls.__verify(user=user, instance=bank)
        return bank

    @classmethod
    def __verify_card(
        cls, cockroach_client: CockroachDBClient, user: User, card_id: UUID
    ) -> CreditCard:
        card: CreditCard = cockroach_client.query(
            CreditCard.get_id,
            id=card_id,
            error_not_exist=False,
        )
        cls.__verify(user=user, instance=card)
        return card

    @classmethod
    def __verify_loan(
        cls, cockroach_client: CockroachDBClient, user: User, loan_id: UUID
    ) -> Loan:
        loan: Loan = cockroach_client.query(
            Loan.get_id,
            id=loan_id,
            error_not_exist=False,
        )
        cls.__verify(user=user, instance=loan)
        return loan

    @classmethod
    def __verify_emi(
        cls, cockroach_client: CockroachDBClient, user: User, emi_id: UUID
    ) -> EMI:
        emi: EMI = cockroach_client.query(
            EMI.get_id,
            id=emi_id,
            error_not_exist=False,
        )
        cls.__verify(user=user, instance=emi)
        return emi

    @classmethod
    def update_bank_balance(cls, db: Session, amount: float, id: UUID, user_id: UUID):
        db.execute(
            text(
                "UPDATE banks SET balance = balance + :amount WHERE id = :id and disabled is NULL and user_id = :user_id"
            ),
            {"amount": amount, "id": id, "user_id": user_id},
        )

    @classmethod
    def update_bank_balance_deprecated(cls, db: Session, amount: float, id: UUID):
        db.execute(
            text(
                "UPDATE banks SET balance = balance + :amount WHERE id = :id and disabled is NULL"
            ),
            {"amount": amount, "id": id},
        )

    @classmethod
    def update_credit_card_balance(cls, db: Session, amount: float, id: UUID):
        db.execute(
            text("UPDATE cards SET pending = pending - :amount WHERE id = :id"),
            {"amount": amount, "id": id},
        )

    @classmethod
    def pay_transaction(
        cls,
        db: Session,
        cockroach_client: CockroachDBClient,
        request: CreateTransactionRequest,
        user: User,
        to_account_id: UUID | None,
        to_account_type: HolderType,
    ):
        if (
            request.amount is not None
            and request.amount < 0
            and (
                request.from_account_id is not None
                or request.from_credit_card_id is not None
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pls Check Details",
            )
        if (
            request.from_account_id is not None
            and request.from_credit_card_id is not None
            and request.from_loan is not None
            and request.from_emi is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pls Check Details",
            )
        if request.from_account_id is not None:
            bank: Bank = cls.__verify_bank(
                cockroach_client, user, request.from_account_id
            )
            Transaction.add(
                db,
                items=[
                    Transaction(
                        user_id=user.id,
                        from_account_id=bank.id,
                        from_account_type=HolderType.bank,
                        to_account_id=to_account_id,
                        to_account_type=to_account_type,
                        amount=request.amount,
                        remarks=request.remarks,
                    )
                ],
            )
            cls.update_bank_balance(
                db, amount=((request.amount) * -1), id=bank.id, user_id=user.id
            )
        elif request.from_credit_card_id is not None:
            card: CreditCard = cls.__verify_card(
                cockroach_client, user, request.from_credit_card_id
            )
            Transaction.add(
                db,
                items=[
                    Transaction(
                        user_id=user.id,
                        from_account_id=card.id,
                        from_account_type=HolderType.credit_card,
                        to_account_id=to_account_id,
                        to_account_type=to_account_type,
                        amount=request.amount,
                        remarks=request.remarks,
                    )
                ],
            )
            cls.update_credit_card_balance(
                db, amount=((request.amount) * -1), id=card.id
            )
        if request.from_loan is not None:
            loan_req = request.from_loan
            loan: Loan = Loan(
                user_id=user.id,
                name=loan_req.name,
                bank_name=loan_req.bank_name,
                total_amount=loan_req.amount,
                pending=loan_req.amount,
                remarks=loan_req.remarks,
            )
            Loan.add(
                db,
                items=[loan],
            )
            Transaction.add(
                db,
                items=[
                    Transaction(
                        user_id=user.id,
                        from_account_id=loan.id,
                        from_account_type=HolderType.loan,
                        to_account_id=to_account_id,
                        to_account_type=to_account_type,
                        amount=loan_req.amount,
                        remarks=request.remarks,
                    )
                ],
            )
        elif request.from_emi is not None:
            emi_req = request.from_emi
            emi: EMI = EMI(
                user_id=user.id,
                name=emi_req.name,
                bank_name=emi_req.bank_name,
                pending=(emi_req.monthly * emi_req.total_time),
                monthly=emi_req.monthly,
                total_time=emi_req.total_time,
                remarks=emi_req.remarks,
            )
            EMI.add(
                db,
                items=[emi],
            )
            Transaction.add(
                db,
                items=[
                    Transaction(
                        user_id=user.id,
                        from_account_id=emi.id,
                        from_account_type=HolderType.emi,
                        to_account_id=to_account_id,
                        to_account_type=to_account_type,
                        amount=emi_req.amount,
                        remarks=request.remarks,
                    )
                ],
            )

    @classmethod
    def get_transaction(
        cls,
        db: Session,
        cockroach_client: CockroachDBClient,
        request: CreateTransferTransactionRequest,
        user: User,
        from_account_id: UUID | None,
        from_account_type: HolderType,
    ):
        if request.amount is not None and request.amount < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pls Check Details",
            )
        if request.to_account_id is not None:
            bank: Bank = cls.__verify_bank(
                cockroach_client, user, request.to_account_id
            )
            Transaction.add(
                db,
                items=[
                    Transaction(
                        user_id=user.id,
                        from_account_id=from_account_id,
                        from_account_type=from_account_type,
                        to_account_id=bank.id,
                        to_account_type=HolderType.bank,
                        amount=request.amount,
                        remarks=request.remarks,
                    )
                ],
            )
            cls.update_bank_balance(
                db, amount=request.amount, id=bank.id, user_id=user.id
            )
        elif request.to_credit_card_id is not None:
            card: CreditCard = cls.__verify_card(
                cockroach_client, user, request.to_credit_card_id
            )
            Transaction.add(
                db,
                items=[
                    Transaction(
                        user_id=user.id,
                        from_account_id=from_account_id,
                        from_account_type=from_account_type,
                        to_account_id=card.id,
                        to_account_type=HolderType.credit_card,
                        amount=request.amount,
                        remarks=request.remarks,
                    )
                ],
            )
            cls.update_credit_card_balance(db, amount=request.amount, id=card.id)
        elif request.to_loan_id is not None:
            loan: Loan = cls.__verify_loan(cockroach_client, user, request.to_loan_id)
            db.execute(
                text("UPDATE loans SET pending = pending - :amount WHERE id = :id"),
                {"amount": request.amount, "id": loan.id},
            )
            Transaction.add(
                db,
                items=[
                    Transaction(
                        user_id=user.id,
                        from_account_id=from_account_id,
                        from_account_type=from_account_type,
                        to_account_id=loan.id,
                        to_account_type=HolderType.loan,
                        amount=request.amount,
                        remarks=request.remarks,
                    )
                ],
            )
        elif request.to_emi_id is not None:
            emi: EMI = cls.__verify_emi(cockroach_client, user, request.to_emi_id)
            db.execute(
                text("UPDATE emis SET pending = pending - :amount WHERE id = :id"),
                {"amount": request.amount, "id": emi.id},
            )
            Transaction.add(
                db,
                items=[
                    Transaction(
                        user_id=user.id,
                        from_account_id=from_account_id,
                        from_account_type=from_account_type,
                        to_account_id=emi.id,
                        to_account_type=HolderType.emi,
                        amount=request.amount,
                        remarks=request.remarks,
                    )
                ],
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pls Check Details",
            )
