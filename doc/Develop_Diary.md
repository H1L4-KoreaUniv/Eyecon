# Develop Diary

## 2020.08.05(Wed)

1. 4분할된 화면 영역의 gaze-estimation 데이터 생성을 위한 ppt 프로그램 구축 
2. Plan A data 생성 및 전처리
3. Dropbox(Data 공유) 생성
4. https://github.com/ADI10HERO/GazeControl 
    1) openvino import 성공
    2) 그러나 opensource code 중 너무 많은 code가 현재 openvino version과 다름
    3) inputs 함수 사용 불가, 대신 input_info class 접근해서 코드 변경
    4) 코드 변경 후 다른 수 많은 에러 생김..
5. generate_metadata.py 추가
    1) metadata.json
        - head pose estimation model을 이용한 pitch, roll, yaw값
        - label 
        - filename 
        - facepoints값
    2) load json
    3) write json
6. dropbox에 label raw data 추가(4사분면 기준으로 labeling)
7. model 생성을 위한 tensorflow 공부
8. haarcasecade estmate 결과가 부정확하여 68_face_landmarks 기반으로 우안,좌안 boundery box 획득
9. Conv2D 기초 모델 생성


## 2020.08.06(Thu)
1. data 생성
    - Eyecon_아이디어_구체화_0805.pdf 파일 내용과 같이 label0~4, 7개의 pose를 고려해 동영상 촬영(각 약 1분)
    - 총 10000개의 데이터 생성
    - 동영상 데이터 이미지 데이터로 변환


## 2020.08.07(Fri)
1.  새로운 headpose_estimation code 참고
    1) https://github.com/qhan1028/Headpose-Detection
    2) 1 ) opensource에서 image로 안경쓴 사진을 넣을 때 얼굴 랜드마크를 잘 찾지 못해 정확하지 못한 값 return
    3) 2 )문제 해결을 위해 headpose_video.py 코드를 수정해 video를 input으로 하여 1초당 해당 프레임의 pitch yaw roll 값을 알 수 있도록 해결
2. 이미지 파일 중 얼굴 랜드마크만 따로 캡처(데이터 전처리)
    1) 1-1) opensource에서 나타내는 랜드마크 좌표값 이용
3. label된 이미지를 feature로만 사용해 딥러닝 
    1) 동영상 이미지로 변환(이때, 파일명에 유의!)
    2) 이미지별 label정보 json 변환
    3) CNN모델 생성

