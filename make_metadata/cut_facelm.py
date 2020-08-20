import cv2


def get_facelm_img(bbox, original):
    x1 = int(bbox[0])
    y1 = int(bbox[1])
    y2 = int(bbox[3])
    facelm_img = cv2.resize(original[y1:y2, x1:x1 + y2 - y1], dsize=(300, 300), interpolation=cv2.INTER_AREA)
    return facelm_img