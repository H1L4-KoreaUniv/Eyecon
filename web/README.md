# C'mon Web System

![image](https://user-images.githubusercontent.com/43233184/91686002-0c77fa80-eb97-11ea-938e-dd2eca56c908.png)
교사의 가르침과 학생의 배움이 하나가 될 때 비로소 올바른 교육의 실천이라고 말할 수 있습니다.<br>
가르침과 배움의 간극이 넓어지는 온라인 교육환경에서<br>
C'mon은 수업의 본질에 집중해 그 간극을 좁히는 온라인 수업 서비스입니다.



## Web System Architecture

![image](https://user-images.githubusercontent.com/43233184/91658530-d9d0f200-eb03-11ea-90bc-326f41c8dd5f.png)


## Installing

Install and update using pip:

```python
$ pip install flask
$ pip install flask-socketio
$ pip install flask-sqlalchemy
$ pip install flask-login
```

## Repository

```
└── web
        ├── chart_data
        ├── generate_data
        ├── live_test
        │   ├── model
        ├── static
        │   ├── assets
        │   │   └── img
        ├── templates
        │   ├── class
        │   ├── login
        │   ├── professor
        │   ├── result
        ├── app.py
```

1. generate_data

    : model input에 필요한 data preprocessing

    - cut_eyelm.py
    - cut_facelm.py
    - headpose.py
    - util.py
    - time.py
2. chart_data

    : professor page.html, class_result.html, my_result.html에 필요한 차트에 대한 데이터 생성

    - meta_process.py
    - metadata.py
3. live_test

    : 학생들의 수업 참여도를 판단하기 위한 webcam live streaming

    - get_frame.py
    - live.py
    - live_process.py
4. static/assets/img

    : web에 사용된 img 저장

5. templates

    : web 구현을 위한 html 파일 저장

## Main Features

1. **webcam real-time streaming**
2. model predict 결과를 바탕으로 **real-time output image streaming**
    - 사용 기술:
        - threading
3. 일정 시간 동안 수업 참여 비율이 낮을 때 학습자에게 **real-time alarm** 보내기
    - 사용 기술:
        - socket
        - javascript SweetAlert
4. 수업 참여 정보를 바탕으로 **real-time chart** 그리기
    - 사용 기술:
        - Chartjs
    - 차트 종류:
        - 교수자를 위한 실시간 학습자 전체의 수업 참여도 정보
        - 교수자를 위한 수업 종료 후 학습자 전체의 수업 참여도 정보
        - 학습자를 위한 수업 종류 후 나의 수업 참여도 정보

## Demo
### Before run
1. Add your model from live_test/model directory

```python
# live_process.py
59   facelm_img = (facelm_img / 255.0).reshape(1, 152,152, 3)
60   lefteyelm_img = (lefteyelm_img / 255.0).reshape(1, 224,224, 3)
61   righteyelm_img = (righteyelm_img / 255.0).reshape(1, 224, 224, 3)

# cut_facelm.py
10  facelm_img = cv2.resize(original[y1:y2, x1:x1 + y2 - y1], dsize=(152, 152), interpolation=cv2.INTER_AREA)

# cut_eyelm.py
23   lefteye_img = cv2.resize(image[eye0y1:eye0y2, eye0x1:eye0x2], dsize=(224, 224), interpolation=cv2.INTER_AREA)
24   righteye_img = cv2.resize(image[eye1y1:eye1y2, eye1x1:eye1x2], dsize=(224, 224), interpolation=cv2.INTER_AREA)
```

2. model input에 맞게 size를 수정하세요.

```python
$ python app.py
```

🎥 [**Demo_video**](https://drive.google.com/file/d/1URumJlHoDgkaJyyPHYp6kwAjmstywiL6/view)

## Notes

현재 C'mon은 local 기반 시스템으로 제작되어 있습니다.

professor와 student가 한 번에 로그인될 수 없는 특징으로 인해 몇가지 주의사항이 있습니다.

1. teacher로 로그인시
    - Chart메뉴를 사용할 경우 회원가입된 학생 전체의 결과가 출력됩니다.
    - 실시간 누적 수업 참여도 그래프의 경우 맨 앞 bar만 실시간 결과를 반영하고 나머지는 랜덤값을 출력합니다.
2. student로 로그인시
    - 과목별 수업 참여도 그래프의 경우 This time을 제외하고 임의의 값이 등록되어 있습니다.

## Future Plans

1. C'mon local 기반의 시스템이 아닌 실제 서버 기반의 시스템이 될 것입니다.
2. 교수자를 위한 수업 관리 페이지를 제작할 것입니다. 이를 통해 교수자는 자신의 여러 수업에 대한 학생들의 결과를 확인할 수 있습니다.
3. 교수자를 위한 Chart에서 여러 학습자의 평균 정보를 실시간 수업 참여도 그래프에 제공할 것입니다.
4. 학습자가 교수자의 페이지에 접근할 수 없도록 더욱 체계적이고 안전한 웹페이지를 제공할 것입니다.

## References
- [./data](https://github.com/H1L4-KoreaUniv/Eyecon/tree/master/data)
- [https://github.com/animesh-chouhan/flask-webcam](https://github.com/H1L4-KoreaUniv/Eyecon/tree/master/data)
- [https://ron.sh/creating-real-time-charts-with-flask/](https://ron.sh/creating-real-time-charts-with-flask/)
