from uuid import UUID


class BusinessRuleError(Exception):
    error_code = "business_rule_error"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class HospitalNotFoundError(BusinessRuleError):
    error_code = "hospital_not_found"

    def __init__(self, hospital_id: int):
        super().__init__(f"Hospital with id {hospital_id} was not found")


class HospitalBatchNotFoundError(BusinessRuleError):
    error_code = "hospital_batch_not_found"

    def __init__(self, batch_id: UUID):
        super().__init__(f"No active hospitals were found for batch {batch_id}")


class InvalidHospitalDataError(BusinessRuleError):
    error_code = "invalid_hospital_data"
