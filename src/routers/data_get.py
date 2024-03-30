from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.user_auth import VerifiedUser, verify_user
from src.client.cockroach import CockroachDBClient
from src.schemas.user import TransactionResponse
from src.schemas.investment import AssetResponse, FDResponse, StockResponse
from src.schemas.liability import EMIResponse, LoanResponse
from src.schemas.wallet import BankResponse, CreditCardResponse
from src.services.data_get import GetService
from src.utils.client import getCockroachClient

DATA_GET_PREFIX = "/data-get"
data_get_router = APIRouter(prefix=DATA_GET_PREFIX)
ENDPOINT_GET_TRANSACTIONS = "/get-transactions/"  # done
ENDPOINT_GET_BANKS = "/get-banks/"  # done
ENDPOINT_GET_CARDS = "/get-cards/"  # done
ENDPOINT_GET_STOCKS = "/get-stocks/"  # done
ENDPOINT_GET_FDS = "/get-fds/"  # done
ENDPOINT_GET_ASSETS = "/get-assets/"  # done
ENDPOINT_GET_LOANS = "/get-loans/"  # done
ENDPOINT_GET_EMIS = "/get-emis/"  # done
ENDPOINT_GET_BANK = "/{bank_id}/get-bank/"  # done
ENDPOINT_GET_CARD = "/{card_id}/get-card/"  # done
ENDPOINT_GET_STOCK = "/{stock_id}/get-stock/"  # done
ENDPOINT_GET_FD = "/{fd_id}/get-fd/"  # done
ENDPOINT_GET_ASSET = "/{asset_id}/get-asset/"  # done
ENDPOINT_GET_LOAN = "/{loan_id}/get-loan/"  # done
ENDPOINT_GET_EMI = "/{emi_id}/get-emi/"  # done
ENDPOINT_GET_EXPENSE = "/{expense_id}/get-expense/"  # pending


@data_get_router.get(
    ENDPOINT_GET_TRANSACTIONS, response_model=list[TransactionResponse]
)
async def get_transactions(
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_transactions(
        user=verified_user.requesting_user, cockroach_client=cockroach_client
    )


@data_get_router.get(ENDPOINT_GET_BANKS, response_model=list[BankResponse])
async def get_banks(
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_banks(
        user=verified_user.requesting_user, cockroach_client=cockroach_client
    )


@data_get_router.get(ENDPOINT_GET_CARDS, response_model=list[CreditCardResponse])
async def get_cards(
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_cards(
        user=verified_user.requesting_user, cockroach_client=cockroach_client
    )


@data_get_router.get(ENDPOINT_GET_LOANS, response_model=list[LoanResponse])
async def get_loans(
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_loans(
        user=verified_user.requesting_user, cockroach_client=cockroach_client
    )


@data_get_router.get(ENDPOINT_GET_EMIS, response_model=list[EMIResponse])
async def get_emis(
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_emis(
        user=verified_user.requesting_user, cockroach_client=cockroach_client
    )


@data_get_router.get(ENDPOINT_GET_FDS, response_model=list[FDResponse])
async def get_fds(
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_fds(
        user=verified_user.requesting_user, cockroach_client=cockroach_client
    )


@data_get_router.get(ENDPOINT_GET_ASSETS, response_model=list[AssetResponse])
async def get_assets(
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_assets(
        user=verified_user.requesting_user, cockroach_client=cockroach_client
    )


@data_get_router.get(ENDPOINT_GET_STOCKS, response_model=list[StockResponse])
async def get_stocks(
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_stocks(
        user=verified_user.requesting_user, cockroach_client=cockroach_client
    )


@data_get_router.get(ENDPOINT_GET_BANK, response_model=BankResponse)
async def get_bank(
    bank_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_bank(
        id=bank_id,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
    )


@data_get_router.get(ENDPOINT_GET_CARD, response_model=CreditCardResponse)
async def get_card(
    card_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_card(
        id=card_id,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
    )


@data_get_router.get(ENDPOINT_GET_EMI, response_model=EMIResponse)
async def get_emi(
    emi_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_emi(
        id=emi_id,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
    )


@data_get_router.get(ENDPOINT_GET_LOAN, response_model=LoanResponse)
async def get_loan(
    loan_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_loan(
        id=loan_id,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
    )


@data_get_router.get(ENDPOINT_GET_FD, response_model=FDResponse)
async def get_fd(
    fd_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_fd(
        id=fd_id,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
    )


@data_get_router.get(ENDPOINT_GET_ASSET, response_model=AssetResponse)
async def get_asset(
    asset_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_asset(
        id=asset_id,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
    )
