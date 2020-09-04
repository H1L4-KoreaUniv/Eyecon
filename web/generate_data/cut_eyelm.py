import dlib
import cv2

# 랜드마크 좌표 받아서 눈 부분 자르기
def get_eye(landmarks, image):

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

    lefteye_img = cv2.resize(image[eye0y1:eye0y2, eye0x1:eye0x2], dsize=(224, 224), interpolation=cv2.INTER_AREA)
    righteye_img = cv2.resize(image[eye1y1:eye1y2, eye1x1:eye1x2], dsize=(224, 224), interpolation=cv2.INTER_AREA)
    return lefteye_img, righteye_img