from flask import Flask, render_template, request, jsonify
from urllib.request import urlopen as uReq
import main
import logging
logging.basicConfig(filename="scrapper.log", level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def home():
    return render_template("search.html")

@app.route("/result", methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content']
            query = searchString.replace(" ", "+")
            img_src_list = main.imageScrapingProcess(searchString = query)
            return render_template("result.html", results = img_src_list[0:len(img_src_list)-1], name = searchString)
        except Exception as e:
            logging.info(e)
    else:
        return render_template("search.html")
    
app.run()