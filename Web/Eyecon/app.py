import flask
# import socketio
from flask import Flask, render_template, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_login import current_user
from datetime import datetime
import cv2
from webcamvideostream import gen, live_test
import json
import time

from metadata import Meta


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Eyecon.sqlite"
app.config['SECRET_KEY'] = '619619'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = b'aaa!111/'
db = SQLAlchemy(app)
login_manager = LoginManager(add_context_processor=False)
login_manager.init_app(app)

metadata = Meta()


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
    classname = db.Column(db.String)
    pname = db.Column(db.String)
    department = db.Column(db.String)
    Date = db.Column(db.String)
    starttime = db.Column(db.String)
    endtime = db.Column(db.String)
    password = db.Column(db.String)


@login_manager.user_loader
def get(id):
    return User.query.get(id)


@app.route('/', methods=['GET'])
# @login_required
def home():
    print(current_user)
    return render_template('index.html', page='home')


@app.route('/login', methods=['GET'])
def login():
    return render_template('Login/login.html')


#
# @socketio.on('connect', namespace='/mynamespace')
# def connect():
#     emit("response", {'data': 'Connected', 'username': current_user.username})
#
# @socketio.on("request", namespace='/mynamespace')
# def request(message):
#     #queue에 저장
#     pass


@app.route('/register', methods=['GET'])
def register():
    return render_template('Login/register.html')


@app.route('/add_class', methods=['GET'])
def add_class_():
    return render_template('add_class.html', page='add_class')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        login_user(user)
        # flask.flash('Logged in successfully.')
        return "<script>alert('Welcome to Eyecon World!'); " \
               "location.href='/'; </script>"
    else:
        return "<script>alert('Please check your email or password'); " \
               "location.href='/login'; </script>"


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
    classname = request.form['classname']
    department = request.form['department']
    date = request.form['date']
    starttime = request.form['starttime']
    endtime = request.form['endtime']
    pname = current_user.username
    password = request.form['password']
    class_tmp = Class(classname=classname, department=department, Date=date,
                      starttime=starttime, endtime=endtime, pname=pname, password=password)
    db.session.add(class_tmp)
    db.session.commit()
    return redirect('/class')


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')


@app.route('/class', methods=['POST', 'GET'])
def class_():
    # print(Class.query.order_by(Class.class_id.desc()))
    all_class = []
    for row in Class.query.order_by(Class.class_id.desc()):
        dt = datetime.strptime(row.Date, '%Y-%m-%d')
        st = datetime.strptime(row.starttime, '%H:%M')
        et = datetime.strptime(row.endtime, '%H:%M')
        now = datetime.now()
        # print(type(now))
        nowdt = datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")  # %H%M%S
        nowt = datetime.strptime(now.strftime("%H:%M"), "%H:%M")
        # print(type(nowdt)," ",nowt)
        if (dt == nowdt and st < nowt and nowt < et):
            state = '수업중'
        elif ((dt == nowdt and nowt < st) or dt > nowdt):
            state = '수업전'
        else:
            state = '수업끝'
        tmp = {'classname': row.classname,
               'department': row.department,
               'professor': row.pname,
               'Date': row.Date,
               'starttime': row.starttime,
               'endtime': row.endtime,
               'state': state,
               '#': row.class_id
               }
        all_class.append(tmp)
    # print(all_class)
    return render_template('class.html', page='class', info=all_class)


@app.route('/attend_check/class_id=<int:id>', methods=['GET'])
def attend_check(id):
    post = Class.query.filter_by(class_id=id).first()
    return render_template('attend_check.html', post=post)


@app.route('/attend/class_id=<int:id>', methods=['POST'])
def attend(id):
    password = request.form['password']
    check = Class.query.filter_by(class_id=id, password=password).first()
    if check:
        return render_template('attend.html')
    else:
        return "<script>alert('Please check class password'); " \
               "location.href='/attend/class_id<int:id>'; </script>"


# 웹캠을 화면에 스트리밍
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    # capture(cv2.VideoCapture(0))
    # live_test(cv2.VideoCapture(0))
    return Response(live_test(cv2.VideoCapture(0), metadata), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/professor_page')
def processor_page():
    return render_template('professor_page.html')

@app.route('/chart_data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(metadata.pop())
            yield f"data:{json_data}\n\n"
            time.sleep(1)
    return Response(generate_random_data(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run()
