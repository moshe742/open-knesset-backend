from typing import Dict
from pydantic import BaseModel

class ErrorDetail(BaseModel):
    error: str
    msg: str

class ErrorExample(BaseModel):
    summary: str
    value: ErrorDetail

    def to_example_dict(self) -> Dict:
        return {
            "summary": self.summary,
            "value": self.value.dict()
        }

class LimitErrorLessThanExample(ErrorExample):
    summary = "Limit Error Less Than Example"
    value = ErrorDetail(error="ValueError", msg="Can't use limit value under 1")

class LimitErrorMoreThanExample(ErrorExample):
    summary = "Limit Error More Than Example"
    value = ErrorDetail(error="ValueError", msg="Can't use limit value above 10000")

class NoDataFoundError(ErrorExample):
    summary = "No Data Is Returned From Database Example"
    value = ErrorDetail(error="TypeError", msg="No such data exists!")

LIMIT_ERROR = {
    "content": {
    "application/json": {
        "examples": {
            "limit_error_less": LimitErrorLessThanExample().to_example_dict(),
            "limit_error_more": LimitErrorMoreThanExample().to_example_dict()
        }
    }
}
}

NO_DATA_FOUND_ERROR = {
    "content": {
    "application/json": {
        "examples": {
            "no_data_found": NoDataFoundError().to_example_dict()
        }
    }
}
}

