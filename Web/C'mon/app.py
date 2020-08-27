from flask import Flask, render_template, request, redirect, Response
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_login import current_user
from datetime import datetime
import cv2
import json
import time

# 학생 수업 집중도 metadata
from metadata import Meta
from live import webcam
from get_frame import Get_frame
from live_process import Process
from meta_process import process_chart_data

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Eyecon.sqlite"
app.config['SECRET_KEY'] = '619619'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = b'aaa!111/'
db = SQLAlchemy(app)
login_manager = LoginManager(add_context_processor=False)
login_manager.init_app(app)

socketio = SocketIO(app)
metadata = Meta()

Process = Process(metadata)
Frame = Get_frame(Process)


###

# Create User db
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    who = db.Column(db.String, unique=False, nullable=False)

    def is_active(self):
        return True


# Create Class db
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


# @app.route('/', methods=['GET'])
# # @login_required
# def home():
#     print(current_user)
#     return render_template('index.html', page='home')

@app.route('/', methods=['GET'])
def home():
    # print(current_user)
    return render_template('index.html', page='home')


@app.route('/login', methods=['GET'])
def login():
    return render_template('Login/login.html')


# sign in
@app.route('/register', methods=['GET'])
def register():
    return render_template('Login/register.html')


# add class for professor
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
        return "<script>alert('Welcome to Cmon World!'); " \
               "location.href='/'; </script>"
    else:
        return "<script>alert('Please check your email or password'); " \
               "location.href='/login'; </script>"


@app.route('/register', methods=['POST'])
def register_post():
    # print(request.form)
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


# get class list
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


# class password check
@app.route('/attend_check/class_id=<int:id>', methods=['GET'])
def attend_check(id):
    post = Class.query.filter_by(class_id=id).first()
    return render_template('attend_check.html', post=post)


# class password check and enter the class
@app.route('/attend/class_id=<int:id>', methods=['POST'])
def attend_enter(id):
    password = request.form['password']
    check = Class.query.filter_by(class_id=id, password=password).first()
    if check:
        return render_template('attend.html')
    else:
        return "<script>alert('Please check class password'); " \
               "location.href='/attend/class_id<int:id>'; </script>"


# for live chart about student
@app.route('/professor_page')
def professor_page():
    for _ in Process.headpose_list:
        print(_)
    return render_template('professor_page.html')


@app.route('/chart_data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(metadata.pop())

            yield f"data:{json_data}\n\n"
            time.sleep(1)

    return Response(generate_random_data(), mimetype='text/event-stream')


# get result of student Focus Summary
@app.route('/class_result')
def class_result():
    return render_template('class_result.html', data=process_chart_data(metadata))

#
# @app.route('/class_result_chart')
# def class_result_chart():
#     def generate_random_data():
#         for _ in metadata.student_info:
#             yield f"data:{_}\n\n"
#             time.sleep(1)
#
#     return Response(generate_random_data(), mimetype='text/event-stream')


###test

# 나중에 attend로 바#######################
@app.route('/test')
def attend():
    return render_template('test.html')


#######################################

# student's webcam screen
@app.route('/live')
def live():
    return Response(webcam(cv2.VideoCapture(0), Frame), mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('connect', namespace='/testsocket')
def connect():
    emit('response', {'hello': "Hello"})


def gen():
    while True:
        info = Frame.get_frame()  # pil_image_to_base64(camera.get_frame())
        frame = info[0]
        focus = info[1]
        if frame is not None:
            if focus == 1:
                # send message if student did not attend class for 3 minutes
                socketio.emit('message', {"goodbye": "Goodbye"}, namespace='/testsocket')
            # student state(red/blue)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')
        else:
            print("frame is none")


# check whether the students are focused or not
@app.route('/live_process')
def live_process():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # app.run()
    socketio.run(app)
