from fastapi import HTTPException, status


def not_implemented(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=detail)
