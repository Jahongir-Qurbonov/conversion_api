import os
import time

from dramatiq import get_broker, Message
from dramatiq.middleware import CurrentMessage
from dramatiq.results import Results

# from dramatiq.worker import has_results_middleware

from .converter import BaseConverter
from .mixins import ActorMixin

# from .results_middleware import CustomResults


class ConverterWorker(BaseConverter, ActorMixin):
    def __init__(self, backend: Results = None) -> None:
        if backend is None:
            self.broker = get_broker()
            for middleware in self.broker.middleware:
                if isinstance(middleware, Results):
                    self.result_middleware: Results = middleware
                    break
            else:
                raise RuntimeError("The default broker doesn't have a results backend.")

        self.actor(
            self.convert, actor_name="converter", max_retries=0, store_results=True
        )
        self.actor(self._delete, max_retries=0)

        if __name__ != "src.worker.tasks":
            self.in_directory = "files/in/"
        else:
            self.in_directory = "src/files/in/"
        if not os.path.isdir(self.in_directory):
            if os.path.exists(self.in_directory):
                raise Exception("Folder directory error")
            os.makedirs(self.in_directory)

        if __name__ != "src.worker.tasks":
            self.out_directory = "files/out/"
        else:
            self.out_directory = "src/files/out/"
        if not os.path.isdir(self.out_directory):
            if os.path.exists(self.out_directory):
                raise Exception("Folder directory error")
            os.makedirs(self.out_directory)

    def _save(self, file: bytes, in_file_path: str) -> None:
        with open(self.in_directory + in_file_path, "wb") as f:
            f.write(file)

    def _delete(self, file_path: str, result_ttl: int = None):
        if result_ttl is not None:
            time.sleep(result_ttl / 1000)
        if os.path.exists(file_path):
            os.remove(file_path)

    def convert(
        self,
        func_name: str,
        _in_file_path: bytes,
        _out_file_path: str,
        out_file_name: str,
    ):
        message: Message = CurrentMessage.get_current_message()

        result_ttl = self.result_middleware._lookup_options(self.broker, message)[1]
        self.result_middleware.backend.store_result(
            message, {"status": "in process"}, result_ttl
        )

        in_file_path = self.in_directory + _in_file_path
        out_file_path = self.out_directory + _out_file_path

        convertion_func = self.__getattribute__(func_name)
        convertion_func(in_file_path, out_file_path, message, result_ttl)

        self._delete.send(in_file_path)
        self._delete.send(out_file_path, result_ttl)

        return {
            "status": "success",
            "out_file_path": _out_file_path,
            "out_file_name": out_file_name,
        }
