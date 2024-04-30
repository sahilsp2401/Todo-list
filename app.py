from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Flask/Todo-list/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todo'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"
    
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer , primary_key=True)
    fname = db.Column(db.String(200), nullable=False)
    lname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200), nullable=False)
    # authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"{self.id} - {self.fname} - {self.lname}"
    
    def __init__(self,email,password,fname,lname):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        # self.authenticated = True

    def check_password(self,password):
        return self.password == password
    
def create_tables():
    with app.app_context():
        if not os.path.exists("todo.db"):
            db.create_all()

create_tables()

@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/login',methods=['GET','POST'])
def login_page():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user:
            if user.check_password(password):
                return render_template("todo.html",user = user)
            else:
                return redirect('/')
        else:
            return redirect('/')
        
    return redirect("/")

@app.route('/register',methods=['GET','POST'])
def register_page():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']

        user = User(fname=fname,lname=lname,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')

    return render_template("register.html")

@app.route('/about')
def about_page():
    return render_template("about.html")

@app.route('/todo',methods=['GET','POST'])
def todo_add():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        id = request.form['user']
        todo = Todo(title=title,desc=desc,id=id)
        db.session.add(todo)
        db.session.commit()
        user = User.query.filter_by(id=id).first()
        return render_template("todo.html",user=user)
    return render_template("todo.html")

@app.route('/viewtodo/<int:id>')
def view(id):
    allTodo = Todo.query.filter_by(id=id).all()
    return render_template("viewtodo.html",allTodo = allTodo)


@app.route('/delete/<int:sno1>/<int:sno2>')
def delete(sno1,sno2):
    todo = Todo.query.filter_by(sno=sno1).first()
    db.session.delete(todo)
    db.session.commit()
    user = User.query.filter_by(id=sno2).first()
    return render_template("todo.html",user=user)


@app.route('/update/<int:sno1>/<int:sno2>',methods=['GET','POST'])
def update(sno1,sno2):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno1).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        user = User.query.filter_by(id=sno2).first()
        return render_template("todo.html",user=user)
    todo = Todo.query.filter_by(sno=sno1).first()
    return render_template("update.html",todo=todo)

if __name__ == "__main__":
    app.run(debug=True)
