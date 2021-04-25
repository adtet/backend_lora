import flask
from flask import Flask,request,jsonify
import mysql.connector
import datetime
from datetime import date

app = Flask(__name__)

def sql_connection():
    sql = mysql.connector.connect(host="localhost",
                                  user="root",
                                  password="",
                                  database="db_lora")
    return sql

def input_data(tgl,pesan):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO `tb_history`(`tanggal`, `pesan`) VALUES (%s,%s)",(tgl,pesan))
    db.commit()

@app.route('/input/data',methods=['POST'])
def data_input():
    json_data = request.json
    if json_data==None:
        result = {"message": "process failed"}
        resp = jsonify(result)
        return resp, 400
    else:
        if 'pesan' not in json_data:
            result = {"message": "error request"}
            resp = jsonify(result)
            return resp, 401
        else:
            pesan = json_data['pesan']
            time = datetime.datetime.now()
            date = time.strftime("%d-%m-%Y")
            waktu = time.strftime("%H:%M:%S")
            tgl = date+" "+waktu
            input_data(tgl,pesan)
            result = {"message": "Input Success"}
            resp = jsonify(result)
            return resp, 200


if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=3001)
    app.run(port=3001, debug=True)
