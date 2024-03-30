from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from src.auth.user_auth import VerifiedUser, verify_user
from src.client.cockroach import CockroachDBClient
from src.schemas.payment import PaymentRequest
from src.services.data_edit import EditService
from src.utils.client import getCockroachClient

DATA_EDIT_PREFIX = "/data-edit"
data_edit_router = APIRouter(prefix=DATA_EDIT_PREFIX)

ENDPOINT_DELETE_BANK = "/{bank_id}/delete-bank/"  # done
ENDPOINT_DELETE_CARD = "/{card_id}/delete-card/"  # done
ENDPOINT_SELL_STOCKS = "/{stock_id}/sell-stocks/"  # pending
ENDPOINT_SELL_FD = "/{fd_id}/sell-fd/"  # pending
ENDPOINT_SELL_ASSET = "/{asset_id}/sell-asset/"  # pending
ENDPOINT_CLOSE_LOAN = "/{loan_id}/close-loan/"  # done
ENDPOINT_CLOSE_EMI = "/{emi_id}/close-emi/"  # done
ENDPOINT_PAY_EMI = "/{emi_id}/pay-emi/"  # done
ENDPOINT_PAY_LOAN = "/{loan_id}/pay-loan/"  # done
ENDPOINT_PAY_CREDIT_CARD = "/{card_id}/pay-credit-card/"  # done


@data_edit_router.get(ENDPOINT_DELETE_BANK)
async def delete_bank(
    bank_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    EditService.delete_bank(
        bank_id=bank_id,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
    )
    return Response(status_code=status.HTTP_200_OK)


@data_edit_router.get(ENDPOINT_DELETE_CARD)
async def delete_card(
    card_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    EditService.delete_card(
        card_id=card_id,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
    )
    return Response(status_code=status.HTTP_200_OK)


@data_edit_router.get(ENDPOINT_CLOSE_LOAN)
async def close_loan(
    loan_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    EditService.close_loan(
        loan_id=loan_id,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
    )
    return Response(status_code=status.HTTP_200_OK)


@data_edit_router.get(ENDPOINT_CLOSE_EMI)
async def close_emi(
    emi_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    EditService.close_emi(
        emi_id=emi_id,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
    )
    return Response(status_code=status.HTTP_200_OK)


@data_edit_router.post(ENDPOINT_PAY_EMI)
async def pay_emi(
    request: PaymentRequest,
    emi_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    EditService.pay_emi(
        emi_id=emi_id,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
        request=request,
    )
    return Response(status_code=status.HTTP_200_OK)


@data_edit_router.post(ENDPOINT_PAY_LOAN)
async def pay_loan(
    request: PaymentRequest,
    loan_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    EditService.pay_loan(
        loan_id=loan_id,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
        request=request,
    )
    return Response(status_code=status.HTTP_200_OK)


@data_edit_router.post(ENDPOINT_PAY_CREDIT_CARD)
async def pay_credit_card(
    request: PaymentRequest,
    card_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    EditService.pay_credit_card(
        card_id=card_id,
        user=verified_user.requesting_user,
        cockroach_client=cockroach_client,
        request=request,
    )
    return Response(status_code=status.HTTP_200_OK)
