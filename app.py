from flask import Flask, render_template, request, redirect, send_from_directory
from flask_migrate import Migrate
from db_init import db
from models import DressModel, AddCart

app = Flask(__name__)  # in name location of the file
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:gop1999ika@localhost/dress'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ASEDTRGGRCSDE'
app.config['MEDIA_FOLDER'] = 'media'

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/media/<path:filename>')
def media_files(filename):
    return send_from_directory(app.config['MEDIA_FOLDER'], filename)


@app.route('/',methods=['GET','POST'])
def home():
    obj = DressModel.query.all()
    if request.method == "POST":
        search = request.form['search_text']
        if search:
            obj = DressModel.query.filter(DressModel.name.ilike(f'%{search}%')).all()
    return render_template('home.html', my_dress=obj)


# @app.route('/about')
# def about():
#     return render_template('about.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        obj = DressModel()
        obj.id = int(request.form['id'])
        obj.name = request.form['name']
        obj.price = float(request.form['price'])
        obj.image = request.form['image']
        db.session.add(obj)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')


@app.route('/more/<int:id>')
def more(id):
    obj = DressModel.query.get(id)
    return render_template('more.html', my_dress=obj)


@app.route('/addcart/<int:id>')
def addcart(id):
    obj = DressModel.query.get(id)
    cart_obj = AddCart(cart=obj.id)
    db.session.add(cart_obj)
    db.session.commit()
    return redirect('/')


@app.route('/viewcart')
def view():
    obj = AddCart.query.all()
    return render_template('view.html', data=obj)


@app.route('/delete/<int:cart_id>')
def remove(cart_id):
    obj = AddCart.query.get(cart_id)
    db.session.delete(obj)
    db.session.commit()
    return redirect('/viewcart')

if __name__ == '__main__':
    app.run(debug=True)
