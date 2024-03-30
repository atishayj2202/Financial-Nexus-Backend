from src.client.cockroach import CockroachDBClient
from src.db.table.bank import Bank
from src.db.table.credit_card import CreditCard
from src.db.table.user import User
from src.schemas.wallet import BankResponse, CreditCardResponse


class GetService:

    @classmethod
    def get_banks(cls, user: User, cockroach_client: CockroachDBClient) -> list[BankResponse]:
        banks : list[Bank] = cockroach_client.query(
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
            ) for bank in banks
        ]

    def get_cards(cls, user: User, cockroach_client: CockroachDBClient) -> list[CreditCardResponse]:
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

