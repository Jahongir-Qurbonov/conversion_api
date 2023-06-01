from io import BytesIO
from mimetypes import guess_type
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Query, UploadFile, File, Header
from fastapi.responses import Response
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


@router.get("/conversion-types")
@inject
async def conversion_types(
    converter_service: ConverterService = Depends(Provide(Container.converter_service)),
):
    conversions = converter_service.get_conversions()
    return {"conversions": conversions}


@router.post("/upload")
@inject
async def upload(
    convert_to: str,
    file: UploadFile = File(),
    converter_service: ConverterService = Depends(Provide(Container.converter_service)),
):
    if convert_to is None:
        return {"error": "cannot be None"}

    message = converter_service.convert(file, convert_to)
    if "error" in message:
        return message
    response = {
        "file_type": convert_to,
        "convert_from": file.content_type,
    }
    response.update(message)
    return response


@router.get("/download")
@inject
async def check(
    message_id: str,
    converter_service: ConverterService = Depends(Provide(Container.converter_service)),
):
    file = converter_service.get_converted_file(message_id)
    if type(file) is str:
        return {"status": file}
    elif type(file) is tuple:
        if type(file[0]) is bytes:
            headers = {
                "content-type": guess_type(file[1])[0],
                # "accept-ranges": "bytes",
                # "content-encoding": "identity",
                # "content-length": str(file_size),
                # "access-control-expose-headers": (
                #     "content-type, accept-ranges, content-length, "
                #     "content-range, content-encoding"
                # ),
            }
            return Response(file[0], headers=headers, media_type=guess_type(file[1])[0])
    return {"error": "error"}


# @router.get("/download")
# @inject
# async def download(
#     message_id: str,
#     range: str | None = Header(default=None),
#     converter_service: ConverterService = Depends(Provide(Container.converter_service)),
# ):
#     return converter_service.range_requests_response(
#         range, *converter_service.get_file(message_id)
#     )
