import cv2

# face boundarybox 좌표값과 이미지를 인자로 받아 얼굴 부분만 자른 이미지를 리턴하는 함수
def get_facelm_img(rect, original):
    
    x1 = int(rect[0])
    y1 = int(rect[1])
    y2 = int(rect[3])
    
    # resize by 224*224
    facelm_img = cv2.resize(original[y1:y2, x1:x1 + y2 - y1], dsize=(224, 224), interpolation=cv2.INTER_AREA)
    
    return facelm_img
