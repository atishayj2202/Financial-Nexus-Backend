from uuid import UUID

from fastapi import HTTPException
from firebase_admin import auth
from firebase_admin.auth import UserRecord
from starlette import status

from src.client.cockroach import CockroachDBClient
from src.client.firebase import FirebaseClient
from src.db.table.feedback import Feedback
from src.db.table.user import User
from src.schemas.user import (
    RatingRequest,
    UserCreateRequest,
    UserResponse,
    UserUpdateRequest,
)


class UserService:
    @classmethod
    def fetch_user(cls, user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
        )

    @classmethod
    def create_user(
        cls,
        request: UserCreateRequest,
        cockroach_client: CockroachDBClient,
        firebase_client: FirebaseClient,
    ) -> None:
        user: User = User(
            email=request.email,
            name=request.name,
            firebase_user_id=request.firebase_user_id,
        )
        user_firebase: UserRecord = auth.get_user(
            request.firebase_user_id, app=firebase_client.app
        )
        if (
            user_firebase.custom_claims is not None
            and firebase_client.user_key in user_firebase.custom_claims
        ):
            user.id = user_firebase.custom_claims[firebase_client.user_key]
        else:
            auth.set_custom_user_claims(
                request.firebase_user_id,
                {firebase_client.user_key: str(user.id)},
                app=firebase_client.app,
            )
        try:
            cockroach_client.query(
                User.add,
                items=[user],
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already found"
            )

    @classmethod
    def update_user(
        cls, user: User, request: UserUpdateRequest, cockroach_client: CockroachDBClient
    ):
        if request.email is not None and request.email != user.email:
            temp = cockroach_client.query(
                User.get_by_field_unique,
                field="email",
                match_value=request.email,
                error_not_exist=False,
            )
            if temp is not None and temp.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
                )
            user.email = request.email
        if request.name is not None and request.name != user.name:
            temp = cockroach_client.query(
                User.get_by_field_unique,
                field="name",
                match_value=request.name,
                error_not_exist=False,
            )
            if temp is not None and temp.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already exists",
                )
            user.name = request.name
        cockroach_client.query(
            User.update_by_id,
            id=user.id,
            new_data=user,
        )

    @classmethod
    def add_feedback(
        cls, user: User, request: RatingRequest, cockroach_client: CockroachDBClient
    ) -> None:
        cockroach_client.query(
            Feedback.add,
            items=[
                Feedback(
                    from_user_id=user.id, rating=request.rate, feedback=request.comment
                )
            ],
        )

    @classmethod
    def fetch_user_by_id(
        cls, user_id: UUID, cockroach_client: CockroachDBClient
    ) -> UserResponse:
        user: User | None = cockroach_client.query(
            User.get_id, id=user_id, error_not_exist=False
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return cls.fetch_user(user)

    @classmethod
    def get_by_username(
        cls, username: str, cockroach_client: CockroachDBClient
    ) -> UserResponse:
        user: User = cockroach_client.query(
            User.get_by_field_unique,
            field="name",
            match_value=username,
            error_not_exist=False,
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return cls.fetch_user(user)
