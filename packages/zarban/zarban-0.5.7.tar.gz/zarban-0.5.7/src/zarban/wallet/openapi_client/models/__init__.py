# coding: utf-8

# flake8: noqa
"""
    Zarban Wallet API

    API for Zarban wallet services.  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: info@zarban.io
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

# import models into model package
from zarban.wallet.openapi_client.models.admin_redemption_update_request import AdminRedemptionUpdateRequest
from zarban.wallet.openapi_client.models.auth_telegram_request import AuthTelegramRequest
from zarban.wallet.openapi_client.models.balance import Balance
from zarban.wallet.openapi_client.models.bank_info import BankInfo
from zarban.wallet.openapi_client.models.bullet_content import BulletContent
from zarban.wallet.openapi_client.models.coin import Coin
from zarban.wallet.openapi_client.models.coin_config import CoinConfig
from zarban.wallet.openapi_client.models.coin_response import CoinResponse
from zarban.wallet.openapi_client.models.create_child_user_request import CreateChildUserRequest
from zarban.wallet.openapi_client.models.currency import Currency
from zarban.wallet.openapi_client.models.deposit_response import DepositResponse
from zarban.wallet.openapi_client.models.detailed_loan_to_value_options import DetailedLoanToValueOptions
from zarban.wallet.openapi_client.models.email_otp_submit_request import EmailOtpSubmitRequest
from zarban.wallet.openapi_client.models.error import Error
from zarban.wallet.openapi_client.models.error_detail import ErrorDetail
from zarban.wallet.openapi_client.models.external_transaction import ExternalTransaction
from zarban.wallet.openapi_client.models.friend_points import FriendPoints
from zarban.wallet.openapi_client.models.friend_points_response import FriendPointsResponse
from zarban.wallet.openapi_client.models.health_status import HealthStatus
from zarban.wallet.openapi_client.models.jwt_response import JwtResponse
from zarban.wallet.openapi_client.models.kyc_confirm_request import KycConfirmRequest
from zarban.wallet.openapi_client.models.kyc_request import KycRequest
from zarban.wallet.openapi_client.models.kyc_response import KycResponse
from zarban.wallet.openapi_client.models.loan_create_request import LoanCreateRequest
from zarban.wallet.openapi_client.models.loan_plan import LoanPlan
from zarban.wallet.openapi_client.models.loan_plan_response import LoanPlanResponse
from zarban.wallet.openapi_client.models.loan_to_value_options import LoanToValueOptions
from zarban.wallet.openapi_client.models.loans_response import LoansResponse
from zarban.wallet.openapi_client.models.loans_response_list import LoansResponseList
from zarban.wallet.openapi_client.models.login_request import LoginRequest
from zarban.wallet.openapi_client.models.network import Network
from zarban.wallet.openapi_client.models.payment import Payment
from zarban.wallet.openapi_client.models.payment_request import PaymentRequest
from zarban.wallet.openapi_client.models.phone_otp_submit_request import PhoneOtpSubmitRequest
from zarban.wallet.openapi_client.models.profile_response import ProfileResponse
from zarban.wallet.openapi_client.models.redemption import Redemption
from zarban.wallet.openapi_client.models.redemption_request import RedemptionRequest
from zarban.wallet.openapi_client.models.redemption_response import RedemptionResponse
from zarban.wallet.openapi_client.models.referral import Referral
from zarban.wallet.openapi_client.models.referral_response import ReferralResponse
from zarban.wallet.openapi_client.models.repay_loan_request import RepayLoanRequest
from zarban.wallet.openapi_client.models.sign_up_request import SignUpRequest
from zarban.wallet.openapi_client.models.simple_response import SimpleResponse
from zarban.wallet.openapi_client.models.swap_request import SwapRequest
from zarban.wallet.openapi_client.models.swap_response import SwapResponse
from zarban.wallet.openapi_client.models.symbol import Symbol
from zarban.wallet.openapi_client.models.task import Task
from zarban.wallet.openapi_client.models.task_response import TaskResponse
from zarban.wallet.openapi_client.models.telegram_profile import TelegramProfile
from zarban.wallet.openapi_client.models.timestamp import Timestamp
from zarban.wallet.openapi_client.models.transaction import Transaction
from zarban.wallet.openapi_client.models.transaction_response import TransactionResponse
from zarban.wallet.openapi_client.models.transaction_status import TransactionStatus
from zarban.wallet.openapi_client.models.transaction_type import TransactionType
from zarban.wallet.openapi_client.models.update_email_request import UpdateEmailRequest
from zarban.wallet.openapi_client.models.update_phone_request import UpdatePhoneRequest
from zarban.wallet.openapi_client.models.user import User
from zarban.wallet.openapi_client.models.user_error import UserError
from zarban.wallet.openapi_client.models.wallet_balance import WalletBalance
from zarban.wallet.openapi_client.models.withdraw_request import WithdrawRequest
from zarban.wallet.openapi_client.models.withdraw_request_body import WithdrawRequestBody
from zarban.wallet.openapi_client.models.withdraw_request_preview import WithdrawRequestPreview
from zarban.wallet.openapi_client.models.withdraw_request_response import WithdrawRequestResponse
from zarban.wallet.openapi_client.models.withdraw_response_body import WithdrawResponseBody
