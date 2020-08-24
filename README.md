# 빅데이터 청년인재 고려대과정 4조 

# C'mon

CNN based online class MONitoring System

*수업 듣고 싶으면 드루와!! Come ON!*

Convolutional Neural Network를 이용한 이미지 분석 기반의 학습자 모니터링 시스템

# WHAT

포스트 코로나 시대, 비대면 온라인 강의 질 향상을 위한 딥러닝 기반의 사용자 모니터링 시스템

![image](https://user-images.githubusercontent.com/43233184/90980736-34180300-e598-11ea-8be8-88ea989a635c.png)

- For 교수자(Instructor)

    학습자의 웹캠 이미지를 시간별로 분석 및 취합하여 전체 학생들의 수업 참여도 정보 및 통계 자료를 가독성 높은 결과물로 제공

- For 학습자(Students)

    학생 본인의 수업 참여도를 스스로 모니터링 가능, 참여도 측정 결과에 따른 알림 및  통계 자료 제공

# HOW

## Data

### Raw Data

노트북 화면 응시여부를 기준으로 0(화면 밖 응시)과 1(화면 안 응시)로 라벨링된 30명의 웹캠을 통해 촬영된 #시간 영상

### Data Preprocessing

1. raw_data에서 [shape_predictor_68_face_landmarks.dat](https://github.com/H1L4-KoreaUniv/Eyecon/tree/master/make_metadata/model)를 이용해 추출한 총 #장의 얼굴 이미지와 해당 인물의 눈 이미지 #*2장 생성
2. headpose estimation value (pitch-yaw-roll) 추출
3. 채도, 좌우반전, 밝기, 대비, 색조 변환, 노이즈 추가 등 Data augmentation기법을 통해 기존 이미지 변형
4. 해당 데이터를 Pandas Dataframe format으로 저장

## Model

![image](https://user-images.githubusercontent.com/43233184/90980751-53169500-e598-11ea-80dc-94cb02115190.png)

## Web

### Registration page

![image](https://user-images.githubusercontent.com/43233184/90980764-5f9aed80-e598-11ea-8eba-85481abe0e23.png)

- 학생 혹은 교수자에 따라 회원가입 및 로그인

### Creating Class

![image](https://user-images.githubusercontent.com/43233184/90980771-66c1fb80-e598-11ea-85a8-36a0bf7db2a9.png)

- 교수는 자신이 원하는 수업을 개설할 수 있음

### Class list and Verifying

![image](https://user-images.githubusercontent.com/43233184/90980777-73465400-e598-11ea-8ebf-82174079fb13.png)

![image](https://user-images.githubusercontent.com/43233184/90980786-793c3500-e598-11ea-8e7b-cc9ac05eb555.png)

- 학생은 자신의 해당 수업에 수업 비밀번호를 입력하여 Attend

> Chart for Instructor(추후 변경 예정)

![image](https://user-images.githubusercontent.com/43233184/90980790-7e997f80-e598-11ea-983d-c973c65f8730.png)

- 학습자의 수업 참여도 정보를 확인
    - Value 1 : 참여
    - Value 0 : 비참여

### Attend page

- 추후 추가 예정

# Run

- 추후 추가 예정

# Reference

- [https://github.com/qhan1028/Headpose-Detection](https://github.com/qhan1028/Headpose-Detection)
- 김태동, 민병아, 이원욱, 박태준, 김태공, 이중엽, 이인성, 김진우, “온라인 강의시청 맥락에서 사용자 주도의 컨트롤제한을 통한 인지된 비통 제성이 강의 집중에 미치는 영향-심리적반발이론을 중심으로”, HCI Korea 2016 학술대회논문집 초록집 pp. 15-24, 2016. 1.
- 김지혜, "개인 간, 개인 내에서 학습자의 학업불안과 지각된 유능성이 자기모니터링을 매개로 성취에 미치는 영향", 한국교원대학교 대학원 pp. 13-30, 51-59, 2020. 2.
