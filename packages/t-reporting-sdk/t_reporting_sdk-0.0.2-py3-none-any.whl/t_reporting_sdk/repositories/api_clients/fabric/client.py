import logging
from os import environ
from typing import Optional

import requests
from pydantic import BaseModel, Field

from t_reporting_sdk.repositories.api_clients.fabric.auth import JWTAuth


logger = logging.getLogger(__name__)


class FabricClientConfig(BaseModel):
    user_email: str = Field(default=environ.get("FABRIC_USER_EMAIL"), validate_default=True)
    user_otp_secret: str = Field(default=environ.get("FABRIC_USER_OTP_SECRET"), validate_default=True)
    base_url: str = Field(default=environ.get("FABRIC_BASE_URL"), validate_default=True)


class FabricClient:
    def __init__(
        self, 
        config: Optional[FabricClientConfig] = None,
    ):
        config = config or FabricClientConfig()
        fabric_auth = JWTAuth(
            email=config.user_email,
            otp_secret=config.user_otp_secret,
            auth_url=config.base_url + "/verify",
            refresh_url=config.base_url + "/refresh-token",
        )
        self._session = requests.Session()
        self._session.auth = fabric_auth

        # Using the /me endpoint as a temporary solution for reporting.
        # This should be replaced with the actual reporting endpoint when available.
        self._base_url = config.base_url

    def create_agent_run(self, run_id: int) -> None:
        url = f"{self._base_url}/apt/agent-runs"
        json_body = {"run_id": run_id}
        response = self._session.post(
            url=url,
            json=json_body
        )
        # Expecting 201 status code
        response.raise_for_status()
        if response.status_code != 201:
            raise RuntimeError("Failed to create agent run.")

    def create_eva_record(
        self,
        run_id: int,
        status: str,
        exception_type: Optional[str],
        message: str,
        customer_id: str,
        patient_id: str,
        payer_id: str,
        portal: str,
    ) -> None:
        url = f"{self._base_url}/apt/records/eva"
        json_body = {
            "agent_run_id": run_id,
            "status": status,
            "exception_type": exception_type,
            "message": message,
            "customer_id": customer_id,
            "patient_id": patient_id,
            "payer_id": payer_id,
            "portal": portal,
            "description": "placeholder",  # TODO: remove this once no longer required by Fabric API
        }
        response = self._session.post(
            url=url,
            json=json_body,
        )
        response.raise_for_status()
        if response.status_code != 202:
            raise RuntimeError("Failed to eva record.")
