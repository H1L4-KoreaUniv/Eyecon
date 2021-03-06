# C'mon 
### CNN based online class participation MONitoring system

1. 프로젝트 개요: Convolutional Neural Network를 이용한 이미지 분석 기반의 **실시간 온라인 수업 학습자 수업 참여도 모니터링 시스템**
2. 프로젝트 기간: 2020.07.06 ~ 2020.08.31
3. 팀원: 이다혜, 이상헌, 이지원, 이지현, 홍유진

## Main Features

1. 온라인 수업을 듣는 학생들의 **수업 참여 여부를 실시간으로 판단**합니다.
2. 판단한 결과를 바탕으로 선생님과 학생에게 **수업 참여도에 대한 통계자료를 제공**합니다.
3. 학생의 수업 참여도가 낮을 경우 주기적인 **알람**을 통해 수업에 참여하도록 합니다.

## System Architecture

![img](https://user-images.githubusercontent.com/43233184/91653317-7ed6d500-eada-11ea-8ccf-34e720ba21a9.png)

## Repository

```
└── data
└── model
└── web
```

1. [data](https://github.com/H1L4-KoreaUniv/Eyecon/tree/master/data)
    - 모델을 위한 데이터 생성 및 전처리
2. [model](https://github.com/H1L4-KoreaUniv/Eyecon/tree/master/model)
    - 학습자가 수업을 참여하는지 판단하기 위한 model 생성
3. [web](https://github.com/H1L4-KoreaUniv/Eyecon/tree/master/Web)
    - C'mon Web system


## Run

```
1. data directory에서 data에 대한 json 생성
2. json을 이용해 model directory에서 model 생성
3. 생성한 model을 이용해 web system 실행
```

위 과정을 모두 수행하시면 C'mon을 경험하실 수 있습니다!
