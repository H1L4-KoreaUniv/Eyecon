import cv2
import socketio

from headpose import HeadposeDetection
from cut_facelm import get_facelm_img
from cut_eyelm import get_eye
import datetime
import random

# import numpy as np
# import tensorflow as tf

# 모델 불러오기
# model = tf.keras.models.load_model('C:/Users/JIWON/Downloads/ahmoo_model1.h5')
# use model

def check_label(input_meta, model):
    # input_meta[0] 이런식으로 처리하
    # input_feature = facelm_img // 255.0
    # prediction =  model.predict(input_feature)
    # print(np.argmax(prediction))
    return 1  # or 0 # 50% 상이면 1 아니면 0!


# 사용자의 웹캠 화면을 웹에 띄우기 + 10초에 한번씩 프레임 캡쳐 (30fps 기준)
#def process_img(img):



def live_test(camera, meta):
    """Video streaming generator function."""
    # frame per sec 확인
    fps = camera.get(cv2.CAP_PROP_FPS)
    # 몇 초마다 프레임 가져올건지?
    sec = 2
    count = 0
    while camera.isOpened():
        ret, frame = camera.read()
        original = frame.copy()
        if frame is None:
            print("frame is none")
            break
        # frame = cv2.flip(frame, 1)  # 그냥 frame에 출력하면됌
        # ret, jpeg = cv2.imencode('.jpg', frame)
        # # print("after get_frame")
        # if jpeg is not None:
        #     yield (b'--frame\r\n'
        #            b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        # else:
        #     print("frame is none")
        # =================================================================================================================
        # input data 생성
        count += 1
        # print(fps,sec,count)
        # print(count%(fps*sec)) #여기 고쳐야함
        #if count % (fps * sec) == 0:
        if count % (int(fps) * sec) == 0:
            label = None
            filename = 'captured_img/frame' + str(int(count / 300))
            #cv2.imwrite(filename + '.jpg', original)
            hpd = HeadposeDetection(1, 'model/shape_predictor_68_face_landmarks.dat')
            _, angles, bbox = hpd.process_image(frame)
            landmark_coords, _, rect = hpd.get_landmarks(original)
            if (angles is not None) and (landmark_coords is not None):  # head pose 제대로 잡았다는 얘기 (landmark도 ok)
                # head pose 좌표값
                print(angles[0], angles[1], angles[2])
                # 14개 face landmarks (2D) -> headpose.py에서 lm_2d_index_list 확인
                #print(landmark_coords)
                # face boundary box
                #print(bbox)
                # face cut image 가져오기
                try:
                    facelm_img = get_facelm_img(rect, original)
                    lefteyelm_img, righteyelm_img = get_eye(landmark_coords, original)
                    if facelm_img is None:
                        label = 0
                        # cv2.imwrite(filename+'_facelm.jpg', facelm_img)
                    # cv2.imwrite(filename + '_lefteyelm_img.jpg', lefteyelm_img)
                    # cv2.imwrite(filename + '_righteyelm_img.jpg', righteyelm_img)
                except:
                    label = 0  # 에러 뜨면 라벨 0으로 처리해버리기
                # return angles, facelm_img, lefteyelm_img, righteyelm_img
            else:
                label = 0
                print('Head pose detection failed')
                # return None
            # cv2.imwrite("captured_img/frame%d.jpg" % (count/300), frame)
            # print('Saved frame%d.jpg' % (count/300))
            # ===================================================================================================================

            # # get label from model
            # if label != 0:
            #     input_meta = [facelm_img, lefteyelm_img, righteyelm_img, angles]
            #     label = check_label(input_meta)
            #
            # # make metadata for professor_page
            #
            # now = datetime.datetime.now()  # get current time
            # nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
            # meta_dic = {'value': label, 'time': nowDatetime}
            print("meta")
            meta_dic = {'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.randrange(0,2)}
            if meta_dic['value']==0:
                frame = cv2.rectangle(original, (150, 200), (250, 300), (255, 0, 0), -1)

            elif meta_dic['value']==1:
                frame = cv2.rectangle(original, (150, 200), (250, 300), (0, 0, 255), -1)

            meta.push(meta_dic)
            frame = cv2.flip(frame, 1)  # 그냥 frame에 출력하면됌
            ret, jpeg = cv2.imencode('.jpg', frame)
            # print("after get_frame")
            if jpeg is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            else:
                print("frame is none")

# ===================================================================================================================


def gen(camera):
    """Video streaming generator function."""
    while True:
        ret, frame = camera.read()
        if frame is None:
            break
        frame = cv2.flip(frame, 1)
        ret, jpeg = cv2.imencode('.jpg', frame)
        # print("after get_frame")
        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        else:
            print("frame is none")
