if __name__ != "src.worker.converter":
    from pdf2docx import Converter as PDFtoDOCXconverter, parse


class BaseConverter:
    # def _convert_doc_to_pdf(self, file_path: str, out_file: str):
    #     pass

    def _convert_pdf_to_doc(self, file_path: str, out_file_path: str):
        parse(file_path, out_file_path)

    # def _convert_docx_to_pdf(self,  file_path: str, out_file: str):
    #     pass

    def _convert_pdf_to_docx(self, file_path: str, out_file_path: str):
        parse(file_path, out_file_path)
