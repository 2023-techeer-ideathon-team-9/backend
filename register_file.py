from PyPDF2 import PdfReader


def get_text(file):
    reader = PdfReader(file)
    pages = reader.pages
    text = ""
    for page in pages:
        sub = page.extract_text()
        text += sub
    return split_test(text)


def split_test(text):
    result = []
    text = text.split('Q. ')
    for i in text:
        result.append(i.split('A.'))
    return result
