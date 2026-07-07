from fastapi import HTTPException, status


class NotFoundException(HTTPException):

    def __init__(self, detail: str = "Recurso não encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UnauthorizedException(HTTPException):

    def __init__(self, detail: str = "Credenciais inválidas"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(HTTPException):

    def __init__(self, detail: str = "Acesso proibido"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class BadRequestException(HTTPException):

    def __init__(self, detail: str = "Requisição inválida"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ConflictException(HTTPException):

    def __init__(self, detail: str = "Recurso já existe"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InternalServerException(HTTPException):

    def __init__(self, detail: str = "Erro interno do servidor"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


NotFoundError = NotFoundException
UnauthorizedError = UnauthorizedException
ForbiddenError = ForbiddenException
BadRequestError = BadRequestException
ConflictError = ConflictException
InternalServerError = InternalServerException
