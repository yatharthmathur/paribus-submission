from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    BusinessRuleError,
    HospitalNotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HospitalNotFoundError)
    async def handle_hospital_not_found(
        _: Request,
        exc: HospitalNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message, "error_code": exc.error_code},
        )

    @app.exception_handler(BusinessRuleError)
    async def handle_business_rule_error(
        _: Request,
        exc: BusinessRuleError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message, "error_code": exc.error_code},
        )
