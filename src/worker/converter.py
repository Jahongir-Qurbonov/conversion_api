if __name__ != "src.worker.converter":
    from pdf2docx import Converter as PDFtoDOCXconverter, parse


class BaseConverter:
    # def _convert_doc_to_pdf(self, file_path: str, out_file: str, *args):
    #     pass

    def _convert_pdf_to_doc(self, in_file_path: str, out_file_path: str, *args):
        self.result_middleware.backend.store_result(args[0], {"status": 0}, args[1])
        parse(in_file_path, out_file_path)
        self.result_middleware.backend.store_result(args[0], {"status": 100}, args[1])

    # def _convert_docx_to_pdf(self,  file_path: str, out_file: str, *args):
    #     pass

    def _convert_pdf_to_docx(self, in_file_path: str, out_file_path: str, *args):
        self.result_middleware.backend.store_result(args[0], {"status": 0}, args[1])
        parse(in_file_path, out_file_path)
        self.result_middleware.backend.store_result(args[0], {"status": 100}, args[1])
