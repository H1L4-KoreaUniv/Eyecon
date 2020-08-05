# Eyecon

 포스트 코로나 시대의 비대면 강의를 위한 강의의 질 향상을 위한 학습자의 이해도 및 집중도 평가 시스템
 
## 구현 계획

- Plan A
1) 화면을 4등분해 각각의 화면을 보고 있는 데이터 생성
2) 각 데이터의 head pose 값(pitch-yaw-roll) 생성(api 사용)
3) 1), 2)를 feature로 deeplearning

- Plan B
1) 3D eye tracking api를 통해 사진당 3D 좌표 계산
2) 1)에 대한 이미지
3) 1), 2)를 feature로 deeplearning

- Plan C
1) 화면을 본다/안본다로 데이터 생성
2) 각 데이터의 head pose 값(pitch-yaw-roll) 생성(api 사용)
3) 1), 2)를 feature로 deeplearning


## 실행 방법

### Data download

#### samples.pkl
https://drive.google.com/drive/folders/1lxwO-A-VBZCVuKKP1FgE_h0ZgfxUvlR4

#### shape_predictor_68_face_landmarks.dat
http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

## 개발 상황
[doc/Develop_Diary.md](https://github.com/H1L4-KoreaUniv/Eyecon/blob/master/doc/Develop_Diary.md)
