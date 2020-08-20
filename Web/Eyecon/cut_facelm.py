import cv2


def get_facelm_img(rect, original):
    if rect is None:
        return None
    x1 = int(rect[0])
    y1 = int(rect[1])
    y2 = int(rect[3])
    facelm_img = cv2.resize(original[y1:y2, x1:x1 + y2 - y1], dsize=(300, 300), interpolation=cv2.INTER_AREA)
    return facelm_img