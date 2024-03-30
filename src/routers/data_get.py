from fastapi import APIRouter, Depends

from src.auth.user_auth import verify_user, VerifiedUser
from src.client.cockroach import CockroachDBClient
from src.services.data_get import GetService
from src.utils.client import getCockroachClient

DATA_GET_PREFIX = "/data-get"
data_add_router = APIRouter(prefix=DATA_GET_PREFIX)
ENDPOINT_GET_TRANSACTIONS = "/get-transactions/"  # pending
ENDPOINT_GET_BANKS = "/get-banks/"  # done
ENDPOINT_GET_CARDS = "/get-cards/"  # done
ENDPOINT_GET_STOCKS = "/get-stocks/"  # pending
ENDPOINT_GET_FDS = "/get-fds/"  # pending
ENDPOINT_GET_ASSETS = "/get-assets/"  # pending
ENDPOINT_GET_LOANS = "/get-loans/"  # pending
ENDPOINT_GET_EMIS = "/get-emis/"  # pending
ENDPOINT_GET_BANK = "/{bank_id}/get-bank/"  # pending
ENDPOINT_GET_CARD = "/{card_id}/get-card/"  # pending
ENDPOINT_GET_STOCK = "/{stock_id}/get-stock/"  # pending
ENDPOINT_GET_FD = "/{fd_id}/get-fd/"  # pending
ENDPOINT_GET_ASSET = "/{asset_id}/get-asset/"  # pending
ENDPOINT_GET_LOAN = "/{loan_id}/get-loan/"  # pending
ENDPOINT_GET_EMI = "/{emi_id}/get-emi/"  # pending
ENDPOINT_GET_EXPENSE = "/{expense_id}/get-expense/"  # pending

@data_add_router.get(ENDPOINT_GET_BANKS)
async def get_banks(
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_banks(user=verified_user.requesting_user, cockroach_client=cockroach_client)

@data_add_router.get(ENDPOINT_GET_CARDS)
async def get_cards(
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return GetService.get_cards(user=verified_user.requesting_user, cockroach_client=cockroach_client)