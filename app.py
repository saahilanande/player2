from os import error
import re
from flask import Flask, render_template, request,redirect,url_for,session
import pyodbc


server = 'tcp:adbsaahilserver.database.windows.net'
database = 'sqldatabase1'
username = 'serveradmin'
password = 'Spa12345'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)


app = Flask(__name__)
app.secret_key = 'any random string'

@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
            if request.form.get("lbutton"):
                name = request.form["uname"]
                red = request.form["red"]
                green = request.form["green"]
                session['username'] = name

                cursor = cnxn.cursor()
                cursor.execute("delete from rng where name = 'p2'")
                cnxn.commit()

                cursor = cnxn.cursor()
                cursor.execute("insert into rng (name,red,green) VALUES('p2','"+red+"','"+green+"');")
                cnxn.commit()
                return redirect('/main')
                
    else: 
        return render_template('login.html')

@app.route('/logout', methods=["POST", "GET"])
def logout():

    session.pop('username', None)

    return render_template('login.html')

@app.route('/main', methods=["POST", "GET"])
def main():
    if request.method == "POST":
            if request.form.get("lbutton"):
                color = request.form["color"]
                amount = request.form["amount"]

                cursor = cnxn.cursor()
                cursor.execute("UPDATE rng SET "+color+" = '"+amount+"' WHERE name = 'p1';")
                cnxn.commit()
                    
                    
                return redirect('/main')

            else:
                
                return render_template('main.html')

    if request.method == "GET": 

        if 'username' in session:
            user = session['username']

            cursor = cnxn.cursor()
            cursor.execute("select green,red from rng where name = 'p1'")
            win = cursor.fetchone()

            cursor = cnxn.cursor()
            cursor.execute("select green,red from rng where name = 'p2'")
            table = cursor.fetchone()

            if win is not None:
                if win[0] == 0 and win[1] == 0:
                    return render_template('winner.html')
                else:
                    return render_template('main.html' ,user=user,greenn=table[0],redn=table[1])
            else:

                return render_template('main.html' ,user=user,greenn=table[0],redn=table[1])
                

        
        else:
                
           return render_template('login.html')

if __name__ == '__main__':
    app.run(debug =True, host='0.0.0.0')