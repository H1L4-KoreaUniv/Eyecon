
import cv2
import dlib
import time

#%%

cap = cv2.VideoCapture(r'C:\Users\sodaus\Downloads\sodaus\sample.mp4')
time.sleep(1) #warming up
if not cap.isOpened():
  exit()

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
count=0

while True:
    ret, image = cap.read()

    if not ret:
        break
    
    # eyes = eye_cascade.detectMultiScale(image)
    # for (ex,ey,ew,eh) in eyes:
    #     cv2.rectangle(image, (ex, ey), (ex+ew, ey+eh),(0,255,0),2)
    # for eye in eyes:
    # (e0x, e0y, e0w, e0h) = eyes[0]
    # (e1x, e1y, e1w, e1h) = eyes[1]
    # cv2.imshow('eye0', cv2.resize(image[e0x:e0x+e0w,e0y:e0y+e0h], dsize=(50, 50), interpolation=cv2.INTER_AREA))
    # cv2.imshow('eye1', cv2.resize(image[e1x:e1x+e1w,e1y:e1y+e1h], dsize=(50, 50), interpolation=cv2.INTER_AREA))
    
    faces = detector(image)
    for face in faces:
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        # cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)

        landmarks = predictor(image, face)
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(image, (x, y), 2, (255, 0, 0), -1)
            
        eye0_bbox = int((landmarks.part(39).x -landmarks.part(36).x)/2 +10)
        eye0_center_x = int((landmarks.part(39).x + landmarks.part(36).x)/2)
        eye0_center_y = int((landmarks.part(39).y + landmarks.part(36).y)/2)
        eye0x1 = eye0_center_x - eye0_bbox
        eye0x2 = eye0_center_x + eye0_bbox
        eye0y1 = eye0_center_y - eye0_bbox
        eye0y2 = eye0_center_y + eye0_bbox
        
        eye1_bbox = int((landmarks.part(45).x -landmarks.part(42).x)/2 +10)
        eye1_center_x = int((landmarks.part(45).x + landmarks.part(42).x)/2)
        eye1_center_y = int((landmarks.part(45).y + landmarks.part(42).y)/2)
        eye1x1 = eye1_center_x - eye1_bbox
        eye1x2 = eye1_center_x + eye1_bbox
        eye1y1 = eye1_center_y - eye1_bbox
        eye1y2 = eye1_center_y + eye1_bbox
        
        
        face_bbox = int((landmarks.part(30).x -landmarks.part(8).x)/2 +50)
        face_center_x = int((landmarks.part(45).x + landmarks.part(42).x)/2)
        face_center_y = int((landmarks.part(45).y + landmarks.part(42).y)/2)
        facex1 = face_center_x - face_bbox
        facex2 = face_center_x + face_bbox
        facey1 = face_center_y - face_bbox
        facey2 = face_center_y + face_bbox
    # cv2.rectangle(image, (eye0x1,eye0y1), (eye0x2,eye0y2), (0, 0, 255), thickness=2)
   
    cv2.imshow('face', cv2.resize(image[ y1:y2, x1:x1+y2-y1], dsize=(300, 300), interpolation=cv2.INTER_AREA))
    cv2.imshow('right eye',cv2.resize(image[eye0y1:eye0y2,eye0x1:eye0x2], dsize=(100, 100), interpolation=cv2.INTER_AREA))
    cv2.imshow('left eye',cv2.resize(image[eye1y1:eye1y2,eye1x1:eye1x2], dsize=(100, 100), interpolation=cv2.INTER_AREA))
    
    
    # count+=1
    # cv2.imwrite("frame{}.jpg" .format(count),
    #             cv2.resize(image[eye0y1:eye0y2,eye0x1:eye0x2], dsize=(100, 100), interpolation=cv2.INTER_AREA))
  

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
