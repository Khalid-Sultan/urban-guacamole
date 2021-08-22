from pdfminer3.pdfparser import PDFParser
from pdfminer3.pdfdocument import PDFDocument
from pdfminer3.pdfpage import PDFPage

def extract(path):
    def clean(res):
        for key, value in res.items():
            res[key] = str(value)[2:-1] 
            if res[key]=='':
                res[key] = 'Unknown'
        return res
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    cl = None
    if len(doc.info)>0:
        cl = clean(doc.info[0])
        for page in PDFPage.create_pages(doc):
            cl['page_size'] = page.mediabox
            break
    return cl
 