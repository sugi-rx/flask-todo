from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite'

db = SQLAlchemy(app)
class List(db.Model):

    __tablename__ = "lists"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text()) 
    category = db.Column(db.Text()) 
    description = db.Column(db.Text()) 

db.create_all()

@app.route('/')
def index():
    lists = List.query.all()
    return render_template("index.html", lists = lists)

@app.route('/new', methods=["POST"])
def new():
    list = List()
    list.title = request.form["list_create"]
    db.session.add(list)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update', methods=["POST"])
def update():
    id = request.form["list_update"]
    list = List.query.filter_by(id=id).one()
    list.category = request.form["list_category"]
    list.description = request.form["list_description"]
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete', methods=["POST"])
def delete():
    id = request.form["list_delete"]
    list = List.query.filter_by(id=id).one()
    db.session.delete(list)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()