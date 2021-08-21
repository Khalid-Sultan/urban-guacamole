def extract(path):
    from pdfminer3.pdfparser import PDFParser
    from pdfminer3.pdfdocument import PDFDocument
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    return doc.info
 