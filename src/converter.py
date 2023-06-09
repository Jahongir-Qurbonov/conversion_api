import os
import pathlib
import mimetypes
import uuid

from typing import Callable, Union

from fastapi import UploadFile
from dramatiq import Message  # , Broker, Encoder, get_broker, set_broker, set_encoder

# from dramatiq.results.backends.redis import RedisBackend
from dramatiq.results import ResultMissing  # ,Results, ResultBackend
from dramatiq.actor import Actor, P, R

from src.worker.tasks import ConverterWorker


class Converter(ConverterWorker):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.__configure()
        self.convert: Union[Actor[P, R], Callable]

    def __configure(self) -> None:
        self.mime_types = []
        class_attrs = self.__dir__()
        conversion_funcs = [
            _func for _func in class_attrs if _func.startswith("_convert_")
        ]
        for func in conversion_funcs:
            # set mimetypes
            _from, _to = [f".{f}" for f in func[9:].split("_to_")]
            self.mime_types.append(
                mimetypes.types_map[_from] + "-" + mimetypes.types_map[_to]
            )

    def send_task(self, file: UploadFile, convert_to: str) -> dict:
        _convert_from = pathlib.Path(file.filename)
        _convert_to = pathlib.Path(convert_to)

        from_ext = _convert_from.suffix[1:]
        to_ext = _convert_to.suffix[1:]

        try:
            func_name = f"_convert_{from_ext}_to_{to_ext}"
            self.__getattribute__(func_name)
        except AttributeError:
            return {"error": "unsupported type"}

        if _convert_to.suffix:
            out_file_stem = _convert_to.stem
        else:
            out_file_stem = _convert_from.stem
        out_file_name = out_file_stem + "." + to_ext

        __uuid = str(uuid.uuid4())
        in_file_path = __uuid + "." + from_ext
        out_file_path = __uuid + "." + to_ext

        self._save(file.file.read(), in_file_path)

        task: Message[R] = self.convert.send(
            func_name, in_file_path, out_file_path, out_file_name
        )
        return {"status": "submitted", "message_id": task.message_id}

    def get_status(self, message_id: str) -> int | str:
        message = self.convert.message_with_options().copy(message_id=message_id)
        try:
            result = message.get_result()
        except ResultMissing:
            return "result missing"
        except Exception as e:
            return "error in get result"

        return result["status"]

    def get_file(self, message_id: str) -> tuple[str, str] | None:
        message = self.convert.message_with_options().copy(message_id=message_id)
        try:
            result = message.get_result()
        except Exception:
            return None

        _out_file_path = result.get("out_file_path", False)
        if not _out_file_path:
            return None

        out_file_path = self.out_directory + _out_file_path
        if not os.path.exists(out_file_path):
            return None
        return out_file_path, result["out_file_name"]
