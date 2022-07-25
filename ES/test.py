from elasticsearch import Elasticsearch
from PyPDF2 import PdfFileReader
import re, datetime, os, tqdm
es = Elasticsearch('http://127.0.0.1:9200')
count = 66

#저장한 시간 정보가 필요할 경우
def utctime():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def to_els(fname):
    data = {}
    temp = open(fname,'rb')
    pdfread = PdfFileReader(temp)
    if pdfread.isEncrypted:
        pdfread.decrypt('')
    title = pdfread.getDocumentInfo().title
    data['title'] = title
    data['totalPage'] = pdfread.getNumPages()
    data['pages'] = []
    re.compile('가-힣0-9')
    for i in tqdm.tqdm(range(0,data['totalPage']),leave=True):
        page = {}
        try:
            page['content'] = re.sub(r"[^가-힣0-9一-龥(). ]","",pdfread.getPage(i).extractText())
        except Exception as e:
            page['content'] = 'ReadingError : '+str(e)
            continue
        page['pagenumber'] = i+1
        data['pages'].append(page)
    putdata(data)

def putdata(doc):
    global count
    es.index(index = 'books', document=doc, id=count)
    count = count+1

def getBooknames(path):
    books = os.listdir(path)
    return [n for n in books if "pdf" in n]

if __name__ == '__main__':
    path = 'C:/Users/124/Desktop/지명/새한_오프라인/'
    booknames = getBooknames(path)
    for i in tqdm.tqdm(booknames[66:],leave=True):
        to_els(path+i)
