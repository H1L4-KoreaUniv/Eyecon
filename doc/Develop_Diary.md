# Develop Diary

## 2020.08.05(수)

1. 4분할된 화면 영역의 gaze-estimation 데이터 생성을 위한 ppt 프로그램 구축 
2. Plan A data 생성 및 전처리
3. Dropbox(Data 공유) 생성
4. https://github.com/ADI10HERO/GazeControl openvino import 성공
    1) 그러나 opensource code 중 너무 많은 code가 현재 openvino version과 다름
    2) inputs 함수 사용 불가, 대신 input_info class 접근해서 코드 변경
    3) 코드 변경 후 다른 수 많은 에러 생김..
5. generate_metadata.py 추가
    1) metadata.json
        - head pose estimation model을 이용한 pitch, roll, yaw값
        - label 
        - filename 
        - facepoints값
    2) load json, write json
6. dropbox에 label raw data 추가(4분면 기준으로 labeling)
7. model 생성을 위한 tensorflow 공부
8. haarcasecade estmate 결과가 부정확하여 68_face_landmarks 기반으로 우안,좌안 boundery box 획득
9. Conv2D 기초 모델 생성
