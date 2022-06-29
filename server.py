from flask import Flask, request, render_template
from datetime import datetime
from TJproject import DatabaseConnection
import json


app = Flask(__name__)
app.secret_key = 'project test'



@app.route('/')
def home():
    return render_template('home.html')

    

@app.route('/select')
def styleWorldcup():
    try:
        DatabaseConnection().getConnection()
        forecast,_,_ = DatabaseConnection().getForecast(datetime.now().strftime("%Y%m%d"))
        imgList = DatabaseConnection().getImagesForWorldcup(forecast[-1], 10)
        DatabaseConnection().closeConnection()

        return render_template('select.html', imgList=imgList) 

    except:
        raise



@app.route('/result')
def showResults():
    try:
        style = request.args.get("style")
        print(style)
        DatabaseConnection().getConnection()
        forecast, weather, temperature = DatabaseConnection().getForecast(datetime.now().strftime("%Y%m%d"))
        results = DatabaseConnection().getResults(weather, temperature, style)
        DatabaseConnection().closeConnection()
        
        print(results)

        return render_template('result.html', forecast=forecast, results=results, style=style)

    except:
        raise



@app.route('/service')
def about():
    return render_template('about1.html')



@app.route('/team')
def members():
    return render_template('member.html')



@app.route('/process')
def process():
    DatabaseConnection().getConnection()
    tbName, tbList = DatabaseConnection().processTable()
    siName, siList = DatabaseConnection().similarTable()
    DatabaseConnection().closeConnection()
    
    return render_template('process.html', tbList=tbList, tbName=tbName, siName=siName, siList=siList)



app.run(host='0.0.0.0', port=9999, debug=True)
