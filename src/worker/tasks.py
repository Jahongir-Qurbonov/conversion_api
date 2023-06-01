import os

from dramatiq.middleware import CurrentMessage

from .converter import BaseConverter
from .utils import ActorMixin


class ConverterWorker(BaseConverter, ActorMixin):
    def __init__(self) -> None:
        self.actor(self.convert, max_retries=0, store_results=True)

        self.__directory = "files/"
        if not os.path.isdir(self.__directory):
            os.mkdir(self.__directory)

    def __save(self, file: bytes, file_path: str) -> None:
        with open(file_path, "wb") as f:
            f.write(file)

    def __delete(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)

    def __get_bytes(self, file_path: str):
        with open(file_path, "rb") as f:
            file = f.read()
        return file

    def convert(
        self,
        func_name: str,
        file: bytes,
        from_ext: str,
        to_ext: str,
        out_file_name: str,
    ):
        message_id = CurrentMessage.get_current_message().message_id

        file_path = self.__directory + message_id + "." + from_ext
        out_file_path = self.__directory + message_id + "." + to_ext

        self.__save(file, file_path)

        convertion_func = self.__getattribute__(func_name)
        convertion_func(file_path, out_file_path)

        _bytes = self.__get_bytes(out_file_path)
        self.__delete(file_path)
        self.__delete(out_file_path)

        return _bytes, out_file_name
