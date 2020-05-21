#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import sqlite3
import datetime
from flask import Flask, render_template, request, session, redirect, g


#sys.path.append("")

username = "user"
password = "password"
DATABASE = "blogdata"

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.context_processor
def cur_date():
    return {'cur_date': datetime.date.today()}



@app.route('/', methods = ['GET'])
def index():
    cur = get_db().cursor()
    cur.execute('select TITLE, AUTHOR, CONTENT, DATETIME from POST')
    p_list = [dict(title = row[0], author = row[1], content = row[2], datetime = row[3]) for row in cur.fetchall()]
    return render_template('index.html', p_list = p_list)
   


@app.route('/login', methods = ['GET', 'POST']) 
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if request.form['username'] == 'user' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect('/dashboard')
        else:
            flash('Invalid login')
            return render_template('login.html', error = error)
        
        

@app.route('/dashboard', methods = ['GET'])
def dashboard():
    if session['logged_in'] == True:
        cur = get_db().cursor()
        cur.execute('select ID, TITLE from POST')
        d_list = [dict(id = row[0], title = row[1]) for row in cur.fetchall()]
        return render_template("dashboard.html", d_list = d_list)
    else:
        return redirect('/login')

        
        
@app.route('/post/add', methods = ['GET','POST'])
def addnewpost():
    error = None
    if session['logged_in'] == True:
        if request.method == 'GET':
            return render_template("addpost.html")
        elif request.method == 'POST':
            cur = get_db().cursor()
            cur.execute('insert into POST (TITLE, AUTHOR, CONTENT, DATETIME) values (?,?,?,?)',(request.form['title'],request.form['author'], request.form['content'], request.form['datetime']))
            get_db().commit()
            return redirect('/dashboard')
        else:
            flash("Error adding Post")
            return redirect('/post/add')
    else:
        return redirect('/login')
        

        
@app.route('/post/<id>', methods = ['GET','POST'])
def modifypost(id):
    error = None
    cur = get_db().cursor()
    if session['logged_in'] == True:
        if request.method == 'GET':
            cur.execute('select TITLE, AUTHOR, CONTENT from POST where ID = ?',(id))
            pp_list = [dict(title = row[0], author = row[1], content = row[2]) for row in cur.fetchall()]
            return render_template("modifypost.html", pp_list = pp_list)
        elif request.method == 'POST':
            t = request.form['title']
            a = request.form['author']
            c = request.form['content']
            d = request.form['datetime']
            i = id
            cur.execute('update post SET TITLE = ?, AUTHOR = ?, CONTENT = ?, DATETIME = ? WHERE id = ?', (t, a, c, d, i))
            get_db().commit()
            return redirect('/dashboard')
        else:
            flash("Error updating Post")
            return redirect('/post/<id>')
    else:
        return redirect('/login')


@app.route('/delete/<id>', methods = ['POST'])
def delpost(id):
    cur = get_db().cursor()
    cur.execute('DELETE from POST where ID = ?',(id))
    get_db().commit()
    return redirect('/dashboard')
   
        
    

if __name__ == '__main__':
    app.secret_key = 'jhntp92uvnp948yubq'
    app.run()


# In[ ]:




