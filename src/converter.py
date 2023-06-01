import pathlib
import mimetypes

from typing import Callable, Union

from fastapi import UploadFile
from dramatiq import Message \
    # , Broker, Encoder, get_broker, set_broker, set_encoder
# from dramatiq.results.backends.redis import RedisBackend
from dramatiq.results import ResultMissing  # ,Results, ResultBackend
from dramatiq.actor import Actor, P, R

from src import worker


class Converter(worker.ConverterWorker):
    def __init__(
            self,
            # broker: Broker,
            # encoder: Encoder,
            # result_middleware: Results,
            # result_backend: RedisBackend,
    ) -> None:
        # self.__broker = broker
        # self.__encoder = encoder
        # self.__result_middleware = result_middleware

        self.convert: Union[Actor[P, R], Callable]
        super().__init__()
        self.__configure()

    def __configure(self) -> None:
        # configure dramatiq
        # self.__broker.add_middleware(self.__result_middleware)

        # set_broker(self.__broker)
        # set_encoder(self.__encoder)

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
        _convert_from = pathlib.Path(args=[file.filename])
        _convert_to = pathlib.Path(convert_to)

        from_ext = _convert_from.suffix[1:]
        to_ext = _convert_to.suffix[1:]

        try:
            func_name = f"_convert_{from_ext}_to_{to_ext}"
            self.__getattribute__(func_name)
        except AttributeError:
            return {"error": "unsupported type"}
            # raise UnsupportedTypeException("unsupported type")

        if _convert_to.suffix:
            out_file_stem = _convert_to.stem
        else:
            out_file_stem = _convert_from.stem
        out_file_name = out_file_stem + "." + to_ext

        task: Message[R] = self.convert.send(
            args=(func_name, file.file.read(), from_ext, to_ext, out_file_name)
        )
        return {"status": "send", "message_id": task.message_id}

    def get_converted_file(self, message_id: str) -> object | str:
        message = self.convert.message_with_options().copy(message_id=message_id)
        try:
            result = message.get_result()
        except ResultMissing:
            return "result missing"
        except Exception as e:
            return "error"
        return result

    def get_file(self, message_id: str):
        message = self.convert.message_with_options().copy(message_id=message_id)
        print(message_id)
        try:
            result = message.get_result()
            print(type(result))
        except:
            return "result missing"
        return message_id
