from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from src.auth.user_auth import VerifiedUser, verify_user
from src.client.cockroach import CockroachDBClient
from src.client.firebase import FirebaseClient
from src.schemas.user import (
    RatingRequest,
    UserCreateRequest,
    UserResponse,
    UserUpdateRequest,
)
from src.services.user import UserService
from src.utils.client import getCockroachClient, getFirebaseClient

USER_PREFIX = "/user"
user_router = APIRouter(prefix=USER_PREFIX)
ENDPOINT_CREATE_USER = "/create-user/"  # done
ENDPOINT_CHECK_USER = "/check-user/"  # done
ENDPOINT_GET_USER = "/get-user/"  # done
ENDPOINT_FIND_USER_BY_ID = "/{user_id}/fetch-user-by-id/"  # done
ENDPOINT_ADD_FEEDBACK = "/add-feedback/"  # done
ENDPOINT_UPDATE_USER = "/update-user/"  # done
ENDPOINT_GET_THREADS = "/get-threads/"  # done
ENDPOINT_ADD_BANK = "/add-bank/"  # pending


@user_router.post(ENDPOINT_CREATE_USER)
async def post_create_user(
    request: UserCreateRequest,
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
    firebase_client: FirebaseClient = Depends(getFirebaseClient),
):
    UserService.create_user(request, cockroach_client, firebase_client)
    return Response(status_code=status.HTTP_200_OK)


@user_router.get(
    ENDPOINT_CHECK_USER,
    dependencies=[Depends(verify_user)],
)
async def get_check_user():
    return Response(status_code=status.HTTP_200_OK)


@user_router.get(ENDPOINT_GET_USER, response_model=UserResponse)
async def get_user(
    verified_user: VerifiedUser = Depends(verify_user),
):
    return UserService.fetch_user(verified_user.requesting_user)


@user_router.post(ENDPOINT_ADD_FEEDBACK)
async def post_add_feedback(
    request: RatingRequest,
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
    verified_user: VerifiedUser = Depends(verify_user),
):
    UserService.add_feedback(
        user=verified_user.requesting_user,
        request=request,
        cockroach_client=cockroach_client,
    )
    return Response(status_code=status.HTTP_200_OK)


@user_router.get(
    ENDPOINT_FIND_USER_BY_ID,
    response_model=UserResponse,
    dependencies=[Depends(verify_user)],
)
async def get_user_by_id(
    user_id: UUID,
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    return UserService.fetch_user_by_id(user_id, cockroach_client)


@user_router.post(ENDPOINT_UPDATE_USER)
async def post_update_user(
    request: UserUpdateRequest,
    verified_user: VerifiedUser = Depends(verify_user),
    cockroach_client: CockroachDBClient = Depends(getCockroachClient),
):
    UserService.update_user(
        user=verified_user.requesting_user,
        request=request,
        cockroach_client=cockroach_client,
    )
    return Response(status_code=status.HTTP_200_OK)
