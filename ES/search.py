from re import S
from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch('http://127.0.0.1:9200')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/pdfview', methods=['POST'])
def pdf_view():
    return render_template('pdfview.html')

@app.route('/pdflist', methods=['GET','POST'])
def pdf_list():
    res = es.search(index="books", source=['title'], body={}, size=200)
    return render_template('pdflist.html', pdflist = res['hits']['hits'])

@app.route('/pdfsearch', methods=['GET','POST'])
def call_pdf():
    req_no = request.form["pdfbtn"]
    res = es.get(index="books", id=req_no)

    return render_template('pdfresult.html', pdffile=res)

@app.route('/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    allsearch = request.form["isall"]

    if allsearch == "on":
        res = es.search(index="books", source=['title'], body={
            "query": {
                "nested":{
                    "path": "pages",
                    "query": {
                        "match": {
                            "pages.content": search_term
                        }
                    },
                    "inner_hits":{
                        "highlight":{
                            "fields" : {
                                "pages.content": {                            
                                    "pre_tags": "<mark>",
                                    "post_tags": "</mark>"
                                }
                            }
                        }
                    }
                }, 
            }}, size=200)
    elif allsearch == 'off':
        res = es.search(index="books", source=['title'], body={
            "query": {
                "nested":{
                    "path": "pages",
                    "query": {
                        "match_phrase": {
                            "pages.content": search_term
                        }
                    },
                    "inner_hits":{
                        "highlight":{
                            "fields" : {
                                "pages.content": {                            
                                    "pre_tags": "<mark>",
                                    "post_tags": "</mark>"
                                }
                            }
                        }
                    }
                }, 
            }}, size=200)

    if res['hits']['total']['value'] == 0:
        return render_template('zero.html', search_term=search_term)

    else:
        return render_template('result.html', res=res, search_term=search_term)
 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)