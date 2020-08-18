import dlib
import cv2

# 랜드마크 좌표 받아서 눈 부분 자르기
def get_eye(landmarks, image):
    # detector = dlib.get_frontal_face_detector()
    # predictor = dlib.shape_predictor(predictor)
    # faces = detector(image)
    # if len(faces) > 0:
    #     for face in faces:
    #         x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
    #         # cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
    #
    # landmarks = predictor(image, face)
    # lm_2d_index_list = [33, 17, 21, 22, 26, 36, 39, 42, 45, 31, 35, 48, 54, 57, 8]
    # for n in lm_2d_index_list:
    #     x = landmarks.part(n).x
    #     y = landmarks.part(n).y

    eye0_bbox = int((landmarks.part(39).x - landmarks.part(36).x) / 2 + 10)
    eye0_center_x = int((landmarks.part(39).x + landmarks.part(36).x) / 2)
    eye0_center_y = int((landmarks.part(39).y + landmarks.part(36).y) / 2)
    eye0x1 = eye0_center_x - eye0_bbox
    eye0x2 = eye0_center_x + eye0_bbox
    eye0y1 = eye0_center_y - eye0_bbox
    eye0y2 = eye0_center_y + eye0_bbox

    eye1_bbox = int((landmarks.part(45).x - landmarks.part(42).x) / 2 + 10)
    eye1_center_x = int((landmarks.part(45).x + landmarks.part(42).x) / 2)
    eye1_center_y = int((landmarks.part(45).y + landmarks.part(42).y) / 2)
    eye1x1 = eye1_center_x - eye1_bbox
    eye1x2 = eye1_center_x + eye1_bbox
    eye1y1 = eye1_center_y - eye1_bbox
    eye1y2 = eye1_center_y + eye1_bbox

    lefteye_img = cv2.resize(image[eye0y1:eye0y2, eye0x1:eye0x2], dsize=(100, 100), interpolation=cv2.INTER_AREA)
    righteye_img = cv2.resize(image[eye1y1:eye1y2, eye1x1:eye1x2], dsize=(100, 100), interpolation=cv2.INTER_AREA)
    return lefteye_img, righteye_img
# else:
#     return None