import flask
from flask import Flask, render_template, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_login import current_user
from datetime import datetime
import cv2
from Eyecon.webcamvideostream import gen, live_test
# from sqlalchemy.sql.functions import user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Eyecon.sqlite"
app.config['SECRET_KEY'] = '619619'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = b'aaa!111/'
db = SQLAlchemy(app)
login_manager = LoginManager(add_context_processor=False)
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    who = db.Column(db.String, unique=False, nullable=False)

    def is_active(self):
        return True


class Class(db.Model):
    class_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classname=db.Column(db.String)
    pname = db.Column(db.String)
    department=db.Column(db.String)
    Date = db.Column(db.String)
    starttime=db.Column(db.String)
    endtime=db.Column(db.String)


@login_manager.user_loader
def get(id):
    return User.query.get(id)


@app.route('/', methods=['GET'])
#@login_required
def home():
    print(current_user)
    return render_template('index.html', page='home')


@app.route('/login', methods=['GET'])
def login():
    return render_template('Login/login.html')


@app.route('/register', methods=['GET'])
def register():
    return render_template('Login/register.html')


@app.route('/add_class', methods=['GET'])
def add_class_():
    return render_template('add_class.html',page='add_class')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email,password=password).first()
    if user:
        login_user(user)
        flask.flash('Logged in successfully.')
        return redirect('/')
    else:
        flask.flash('Please check your email or password')
        return redirect('/login')


@app.route('/register', methods=['POST'])
def register_post():
    print(request.form)
    # print(request.form.getlist('username'))
    # print(request.form['username'])
    username = request.form['username']
    password = request.form['password']
    who = request.form['who']
    email = request.form['email']
    user = User(username=username, password=password, email=email, who=who)
    db.session.add(user)
    db.session.commit()
    # user = User.query.filter_by(email=email).first()
    # login_user(user)
    return redirect('/login')


@app.route('/add_class', methods=['POST'])
def add_class_post():
    classname=request.form['classname']
    department=request.form['department']
    date = request.form['date']
    starttime=request.form['starttime']
    endtime=request.form['endtime']
    pname = current_user.username
    class_tmp = Class(classname=classname,department=department,Date=date,
                      starttime=starttime,endtime=endtime,pname=pname)
    db.session.add(class_tmp)
    db.session.commit()
    return redirect('/class')


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')


@app.route('/class', methods=['POST', 'GET'])
def class_():
    print(Class.query.order_by(Class.class_id.desc()))
    all_class=[]
    for row in Class.query.order_by(Class.class_id.desc()):
        dt = datetime.strptime(row.Date,'%Y-%m-%d')
        st = datetime.strptime(row.starttime,'%H:%M')
        et = datetime.strptime(row.endtime,'%H:%M')
        now = datetime.now()
        print(type(now))
        nowdt=datetime.strptime(now.strftime("%Y-%m-%d"),"%Y-%m-%d") #%H%M%S
        nowt=datetime.strptime(now.strftime("%H:%M"),"%H:%M")
        print(type(nowdt)," ",nowt)
        if (dt==nowdt and st<nowt and nowt<et):
            state='수업중'
        elif ((dt==nowdt and nowt<st) or dt>nowdt):
            state='수업전'
        else:
            state='수업끝'
        tmp={ 'classname': row.classname,
              'department': row.department,
              'professor': row.pname,
              'Date': row.Date,
              'starttime': row.starttime,
              'endtime': row.endtime,
              'state': state,
              '#': row.class_id
            }
        all_class.append(tmp)
    print(all_class)
    return render_template('class.html', page='class', info=all_class)


@app.route('/attend', methods=['POST', 'GET'])
def attend():
    return render_template('attend.html')


###################################################################################################################
# live test

# 웹캠을 화면에 스트리밍
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    # capture(cv2.VideoCapture(0))
    # live_test(cv2.VideoCapture(0))
    return Response(live_test(cv2.VideoCapture(0)), mimetype='multipart/x-mixed-replace; boundary=frame')

###################################################################################################################


if __name__ == '__main__':
    app.run()
