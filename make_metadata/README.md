# Data Description

## Raw Data

- 노트북 화면 응시여부를 기준으로 0(화면 밖 응시)과 1(화면 안 응시)로 라벨링된 영상
- 현재까지 subject 21명의 웹캠 영상 수집 완료, 총 30명을 목표로 수집 진행중

## Data Preprocessing

### Requirements

- openCV

    `pip install opencv-python` 

- dlib

    `pip install cmake`

    `pip install dlib`

- shape_predictor_68_face_landmarks.dat

    [http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)

### Extracted Features

영상 Raw Data를 1초마다 프레임 추출하여 전처리를 통해 아래 4개의 데이터를 생성 

- Feature 1. 68개 face landmarks coordinates
    - pre-trained model(shape_predictor_68_face_landmarks.dat) 사용
    - 68개 점의 좌표를 array로 저장

    <img src="https://images.velog.io/images/choiiis/post/27590ef9-4e31-4728-916f-e03a6f71b463/image.png" width="30%">

- Feature 2. 얼굴 부분만 추출한 이미지
    - face landmarks coodinates를 이용해 얼굴 부분만 crop
    - 300*300으로 resize하여 .jpg 파일로 저장
- Feature 3. 눈 좌우 부분만 각각 추출한 이미지
    - face landmarks coodinates를 이용해 눈 좌우 부분만 각각 crop
    - 100*100으로 resize하여 .jpg 파일로 저장
- feature 4. head-pose estimation value (pitch, yaw, roll)
    - pitch : 고개를 위, 아래로 움직인 각도를 나타내며 위로 움직인 경우 +값을, 아래로 움직인 경우를 -값을 가짐
    - yaw : 고개를 좌, 우로 회전한 각도를 나타내며 좌로 움직인 경우 +값을, 우로 움직인 경우 -값을 가짐
    - roll : 고개를 좌, 우로 기울인 각도를 나타내며 좌로 움직인 경우 +값을, 우로 움직인 경우 -값을 가짐

        <img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/a7e360b1-f139-4e63-9a9d-f611a596570f/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20200824%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20200824T105136Z&X-Amz-Expires=86400&X-Amz-Signature=40947466714d521948f7826f325cb6a3f379e33189e2db45d2a8463e15829ebd&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22" width="30%">

### Usage

`generate_data.py`
`metadata.json`


### Referenced Code

- [https://github.com/qhan1028/Headpose-Detection](https://github.com/qhan1028/Headpose-Detection)
- 

# Exploratory Data Analysis

주피터로 작성한 ipynb
