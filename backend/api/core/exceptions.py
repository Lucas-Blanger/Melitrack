from fastapi import HTTPException, status


class NotFoundError(HTTPException):

    def __init__(self, detail: str = "Recurso não encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UnauthorizedError(HTTPException):

    def __init__(self, detail: str = "Credenciais inválidas"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenError(HTTPException):

    def __init__(self, detail: str = "Acesso proibido"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class BadRequestError(HTTPException):

    def __init__(self, detail: str = "Requisição inválida"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ConflictError(HTTPException):

    def __init__(self, detail: str = "Recurso já existe"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InternalServerError(HTTPException):

    def __init__(self, detail: str = "Erro interno do servidor"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )
