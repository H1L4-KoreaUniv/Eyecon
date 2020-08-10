# Eyecon
---
### Eye Tracking Based Concentration Evaluating System
 포스트 코로나 시대의 비대면 온라인 강의의 질 향상을 위한 학습자의 이해도 및 집중도 평가 시스템

## 개요 
- 대면 강의에 비해 교수자-학습자의 쌍방향 소통이 어려운 비대면 강의에서 교수자가 다수의 학습자의 이해도 및 집중도를 한눈에 파악할 수 있도록 함
- 이를 통해 교수자가 강의 속도 및 난이도를 실시간으로 조절할 수 있도록 보조 함
- 이를 통해 학습자의 집중도를 높이고 이해도 향상에 도움을 줌

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

- [samples.pkl](https://drive.google.com/drive/folders/1lxwO-A-VBZCVuKKP1FgE_h0ZgfxUvlR4)
- [shape_predictor_68_face_landmarks.dat](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)

## 개발 상황
- [Develop_Diary](https://github.com/H1L4-KoreaUniv/Eyecon/blob/master/doc/Develop_Diary.md)
