from flask import Flask,render_template,request,redirect,url_for,g,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key='harshssecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
db=SQLAlchemy(app)

class user(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20))
    password=db.Column(db.String(20))

    def __init__(self,username,password):
        self.username=username
        self.password=password

class posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    data=db.Column(db.String(1000))
    userna=db.Column(db.String(40))

    def __init__(self,title,data,userna):
        self.title=title
        self.data=data
        self.userna=userna

@app.route('/')
def hello_world():
    aa=user.query.all()
    users=[]
    for i in range(len(aa)):
        users.append(aa[i].username)
    zz=posts.query.all()
    ran=range(len(zz))
    return render_template('index.html',zz=zz,ran=ran)

@app.route('/login',methods=["POST","GET"])
def login():
    session.pop('logged_in',None)
    # print("Popped the sessions")
    if request.method=="POST":
        uname=request.form['uname']
        passw=request.form['passw']
        zz=user.query.filter_by(username=uname).first()
        # print(zz.password)
        if zz.password==passw:
            # print("Signing the user in")
            session['logged_in']=uname
            return redirect(url_for('createpost'))
    return render_template('login.html')

@app.route('/signup',methods=["POST","GET"])
def signup():
    if request.method=="POST":
        uname=request.form["uname"]
        passw=request.form["passw"]
        adding=user(username=uname,password=passw)
        db.session.add(adding)
        db.session.commit()
        # print("User added")
    return render_template('signup.html')

@app.route('/createpost',methods=["GET","POST"])
def createpost():
    if request.method=="POST":
        title=request.form['title']
        data=request.form['data']
        adding=posts(title=title,data=data,userna=g.user)
        db.session.add(adding)
        db.session.commit()
    zz=posts.query.filter_by(userna=g.user).all()
    ran=range(len(zz))
    # print(zz)
    return render_template('createpost.html',ran=ran,zz=zz)

@app.before_request
def before_request():
    g.user=None
    if 'logged_in' in session:
        g.user=session['logged_in']

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('hello_world'))

@app.route('/delete/<title>')
def delete(title):
    posts.query.filter_by(title=title).delete()
    db.session.commit()
    return redirect(url_for('createpost'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
