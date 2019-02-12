from flask import Flask,request,jsonify,render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
dictionary = {"definitions":[]}
@app.route('/')
def index():
    return "hello world"

@app.route('/search/<string:query>')
def search(query):
    url = 'https://www.vocabulary.com/dictionary/' + query
    res = requests.get(url)
    html = BeautifulSoup(res.text,features="html.parser")
    
    # : h1 ele text
    h1 = html.select('h1[class="dynamictext"]')[0]
    dictionary['title']= h1.text
    
    # : short defination
    Pshort = html.select('div[class="section blurb"]> p[class="short"]')[0] 
    dictionary['short-summary'] = Pshort.text

    # : long defination
    Plong = html.select('div[class="section blurb"] > p[class="long"]')[0]
    dictionary['long-summary'] = Plong.text

    # : defination
    ## definatio
    ordinal = html.select('h3[class="definition"]')
    for di in ordinal:
        text = di.text.replace('\n','').replace('\t','').replace('\r','')
        dictionary['definitions'].append(text)

    # : return json
    return jsonify(dictionary)
if __name__ == "__main__":
    app.run()
