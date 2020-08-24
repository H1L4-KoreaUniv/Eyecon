# 빅데이터 청년인재 고려대과정 4조 

1. 프로젝트명: C'MON(CNN based online class MONitoring System)
*수업 듣고 싶으면 드루와!! Come ON!*
2. 프로젝트 기간: 2020.07.06 ~ 2020.08.31
3. 팀원: 이다혜, 이상헌, 이지원, 이지현, 홍유진 
4. 프로젝트 개요: Convolutional Neural Network를 이용한 이미지 분석 기반의 비대면 온라인 수업 학습자 모니터링 시스템

# WHAT

포스트 코로나 시대, 비대면 온라인 강의의 질 향상을 위한 딥러닝 기반의 수업 참여도 모니터링 시스템

![image](https://user-images.githubusercontent.com/43233184/90980736-34180300-e598-11ea-8be8-88ea989a635c.png)

본 팀이 구현하는 시스템은 다음과 같이 크게 세 가지 부분으로 나눌 수 있다. 

1. 학습자 화면  

    학습자는 온라인 비대면 수업에 참여함으로써 수업을 듣는 본인의 웹캠 영상을 일정 시간 간격마다 서버에 전송하게 된다.  서버는 이미지 데이터를 받아 학습자의 수업 참여도를 산출하고, 이를 다시 학습자에게 제공하여 본인의 수업 참여 정도를 스스로 모니터링 할 수 있도록 돕는다. 

2. CNN 모델을 포함하는 서버

    서버는 학습자의 이미지 데이터를 받아 CNN 모델을 통한 분석 과정을 거쳐서 학습자가 수업에 잘 참여하고 있는지 혹은 참여하지 않고 있는지를 판단한다.  또한 해당 수업을 수강하는 여러 학습자들의 수업 참여도를 취합한다.  

3. 교수자 화면  

    교수자는 본인의 수업을 수강하는 모든 학습자들의 수업 참여도를 한눈에 알아볼 수 있도록 시각화 된 통계자료를 제공받는다. 이를 통해 수업 난이도 조절 및 학습자의 참여 유도 등 수업의 질을 높이는 데 참고할 수 있으며 학습자에게 피드백을 전달할 수 있다.

# HOW

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
