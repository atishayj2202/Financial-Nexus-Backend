from enum import Enum


class AuthType(Enum):
    google = "google"
    facebook = "facebook"
    github = "github"
    apple = "apple"
    email = "email"
    phone = "phone"


class HolderType(Enum):
    bank = "bank"
    credit_card = "credit_card"
    emi = "emi"
    loan = "loan"
    expense = "expense"
    income = "income"
    stock = "stock"
    fd = "fd"
    asset = "asset"


class MessageBy(Enum):
    user = "user"
    ai = "ai"
