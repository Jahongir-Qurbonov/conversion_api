# from pydantic import BaseModel
from fastapi import APIRouter, Depends, UploadFile, File, Header, status, Response
from dependency_injector.wiring import inject, Provide

from .containers import Container
from .services import ConverterService


# class FileDataIn(BaseModel):
#     file_type: str = Query()
#     convert_to: str = Query()
#     file: UploadFile = File()


# class FileDataOut(BaseModel):
#     file_type: str
#     convert_from: str
#     message_id: str


router = APIRouter(prefix="/converter")


@router.get("/conversion-types", status_code=status.HTTP_200_OK)
@inject
async def conversion_types(
    converter_service: ConverterService = Depends(Provide(Container.converter_service)),
):
    conversions = converter_service.get_conversions()
    return {"conversions": conversions}


@router.post("/upload", status_code=status.HTTP_201_CREATED)
@inject
async def upload(
    convert_to: str,
    response: Response,
    file: UploadFile = File(),
    converter_service: ConverterService = Depends(Provide(Container.converter_service)),
):
    message = converter_service.convert(file, convert_to)
    if "error" in message:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return message
    res = {
        "file_type": convert_to,
        "convert_from": file.content_type,
    }
    res.update(message)
    return res


@router.get("/check", status_code=status.HTTP_200_OK)
@inject
async def check(
    message_id: str,
    response: Response,
    converter_service: ConverterService = Depends(Provide(Container.converter_service)),
):
    status_task = converter_service.get_status(message_id)
    if type(status_task) is int or type(status_task) is str:
        return {"status": status_task}
    else:
        if status == "result missing":
            response.status_code = status.HTTP_404_NOT_FOUND
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": status_task}


@router.get("/download")
@inject
async def download(
    message_id: str,
    response: Response,
    range: str | None = Header(default=None),
    converter_service: ConverterService = Depends(Provide(Container.converter_service)),
):
    _file = converter_service.get_file(message_id)
    if _file is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "file not found"}
    return converter_service.range_requests_response(range, *_file)
