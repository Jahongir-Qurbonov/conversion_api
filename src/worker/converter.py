if __name__ != "src.worker.converter":
    from pdf2docx import Converter as PDFtoDOCXconverter, parse


class BaseConverter:
    # def _convert_doc_to_pdf(self, file_path: str, out_file: str, *args):
    #     pass

    def _convert_pdf_to_doc(self, in_file_path: str, out_file_path: str, **kwargs):
        self.result_middleware.backend.store_result(
            kwargs["message"], {"status": 0}, kwargs["result_ttl"]
        )
        parse(in_file_path, out_file_path)
        self.result_middleware.backend.store_result(
            kwargs["message"], {"status": 100}, kwargs["result_ttl"]
        )

    # def _convert_docx_to_pdf(self,  file_path: str, out_file: str, *args):
    #     pass

    def _convert_pdf_to_docx(self, in_file_path: str, out_file_path: str, **kwargs):
        self.result_middleware.backend.store_result(
            kwargs["message"], {"status": 0}, kwargs["result_ttl"]
        )
        parse(in_file_path, out_file_path)
        self.result_middleware.backend.store_result(
            kwargs["message"], {"status": 100}, kwargs["result_ttl"]
        )
