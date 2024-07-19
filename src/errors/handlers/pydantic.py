from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

# pydantic エラー例
# [
#     {
#         'type': 'greater_than',
#         'loc': ('gt_int',),
#         'msg': 'Input should be greater than 42',
#         'input': 21,
#         'ctx': {'gt': 42},
#         'url': 'https://errors.pydantic.dev/2/v/greater_than',
#     },
# ]


# ミドルウェアで使用しているが @app.exception_handler() でラップして使うこともできる
def validation_error_handler(error: ValidationError):
    first_error = error.errors()[0]
    err_dict = {
        "id": "PYDANTIC_VALIDATION_ERROR",
        "message": first_error.get("msg"),
        "detail": f"valid field: {first_error.get('loc')}, input value: {first_error.get('input')}",
    }

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=err_dict
    )
