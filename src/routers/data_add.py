from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from src.auth.user_auth import VerifiedUser, verify_user
from src.client.cockroach import CockroachDBClient
from src.schemas.income import ExpenseRequest, IncomeRequest
from src.schemas.investment import CreateStockInvestementRequest
from src.schemas.wallet import CreateBankRequest, CreateCreditCardRequest
from src.services.data_add import AddService
from src.utils.client import getCockroachClient

DATA_ADD_PREFIX = "/data-add"
data_add_router = APIRouter(prefix=DATA_ADD_PREFIX)
ENDPOINT_ADD_BANK = "/add-bank/"  # done
ENDPOINT_ADD_CARD = "/add-card/"  # done
ENDPOINT_ADD_INCOME = "/add-income/"  # done
ENDPOINT_ADD_EXPENSE = "/add-expense/"  # done
ENDPOINT_ADD_STOCKS = "/add-stocks/"  # done
ENDPOINT_ADD_FD = "/add-fd/"  # pending
ENDPOINT_ADD_ASSETS = "/add-assets/"  # pending
ENDPOINT_ADD_LOAN = "/add-loan/"  # pending
ENDPOINT_ADD_EMIS = "/add-emis/"  # pending


@data_add_router.post(ENDPOINT_ADD_BANK)
async def post_add_bank(
    request: CreateBankRequest,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    AddService.add_bank(
        request=request,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
    )
    return Response(status_code=status.HTTP_200_OK)


@data_add_router.post(ENDPOINT_ADD_CARD)
async def post_add_card(
    request: CreateCreditCardRequest,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    AddService.add_bank(
        request=request,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
    )
    return Response(status_code=status.HTTP_200_OK)


@data_add_router.post(ENDPOINT_ADD_INCOME)
async def post_add_income(
    request: IncomeRequest,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    AddService.add_income(
        request=request,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
    )
    return Response(status_code=status.HTTP_200_OK)


@data_add_router.post(ENDPOINT_ADD_EXPENSE)
async def post_add_expense(
    request: ExpenseRequest,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    AddService.add_expense(
        request=request,
        user=verified_user.request,
        cockroach_client=cockroach_client,
    )
    return Response(status_code=status.HTTP_200_OK)


@data_add_router.post(ENDPOINT_ADD_STOCKS)
async def post_add_stocks(
    request: CreateStockInvestementRequest,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    AddService.add_stock(
        request=request,
        user=verified_user.request,
        cockroach_client=cockroach_client,
    )