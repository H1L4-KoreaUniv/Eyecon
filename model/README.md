# Model

 딥러닝에 사용한 알고리즘은 이미지 처리에 유용한 Convolutional Neural Network(CNN)입니다. 입력은 얼굴 이미지, 두 눈 이미지, headpose 벡터로 총 4개이며, 2개의 CNN을 사용하였고, 출력은 binary class입니다. 이미지는 26명의 영상에서 13,563장의 frame을 추출하여 총 40,689장입니다.
 
 
## Image Transformation
 영상에서 1초 단위로 프레임을 추출하였기 때문에 연속된 이미지들은 유사한 경우가 있었습니다. 이미지의 분포를 넓게 하여 조금 더 일반화된 가중치를 학습시키고자 이미지에 아래와 같은 변형을 주었습니다.
 
 ![image](https://user-images.githubusercontent.com/61040406/91671156-06662780-eb5f-11ea-9535-f7df072481b4.png)
 원본 이미지의 밝기, 대조, 색조, 채도를 무작위로 변경하고, 노이즈를 랜덤하게 줘서 가장 오른쪽 이미지와 같이 변형을 주어 데이터의 분포를 넓게 만들었습니다.
 

## Transfer Learning

 모델 학습에는 Transfer learning을 적용하였습니다. Transfer learning은 모델이 이미 많은 데이터를 학습하여 일반화된 feature를 가지기 때문에, 학습할 데이터가 적을 때 유용하며 학습 시간을 줄이는 장점이 있습니다. Transfer learning에 고려된 모델은 아래 그림과 같습니다. 

![image](https://user-images.githubusercontent.com/61040406/91663178-3d6a1800-eb22-11ea-93d6-9d1d2afd0ea5.png)

- DeepFace는 Facebook 사용자가 업로드한 400만 개의 얼굴 이미지를 학습하였으며, 약 1억 2천만 개의 가중치를 가집니다.
- VGG16은 1400만 개의 이미지로 이루어진 이미지넷을 학습하였으며, 약 1억 4000만 개의 가중치를 가집니다.
- ResNet50은 이미지넷을 학습하였으며, 약 2500만 개의 가중치를 가집니다.
- MobileNetV2는 이미지넷을 학습하였으며, 약 350만 개의 가중치를 가집니다.


## Model Structure

 ![image](https://user-images.githubusercontent.com/61040406/91663643-2aa51280-eb25-11ea-8a99-bb7c8df9c260.png)

 우리가 개발한 모델을 살펴봅시다. 얼굴 이미지를 입력으로 받는 첫 번째 CNN에는 DeepFace가 사용되었습니다. 양쪽 눈은 두 번째 CNN에 따로 입력됩니다. 두 번째 CNN으로는 VGG16, ResNet50, MobileNetV2를 고려하였고, 최종 모델로 MobileNetV2를 사용하였습니다. 3차원 얼굴 각도는 모델 상단의 fully-connected layer에서 입력됩니다.

 출력은 온라인 수업 화면을 응시하는지, 응시하지 않는지에 대한 binary 예측값입니다.

## Performance

 눈 모델로 VGG16, ResNet50, MobileNetV2를 사용하였을 때의 결과를 비교하였습니다. 아래 결과들을 종합해보면 모든 비교 항목에서 MobileNetV2가 가장 우수하였습니다. 따라서 최종 눈 모델로 MobileNetV2를 사용하였습니다.

### Evaluation
| Model | Validation Loss | Validation Accuracy |
|---|---:|---:|
| VGG16 | 0.0700 | 0.9767 |
| ResNet50 | 0.0788 | 0.9735 |
| MobileNetV2 | 0.0406 | 0.9877 |

![image](https://user-images.githubusercontent.com/61040406/91663276-d436d480-eb22-11ea-81f3-91a734354fda.png)

 MobileNetV2를 사용하였을 때, validation Loss는 다른 두 모델의 절반 수준에 가까웠습니다. 예측 성능은 MobileNetV2가 VGG16보다 1.10%p, ResNet50보다 1.42%p 높았습니다.

### Efficiency
| Model | Time for one epoch | Number of params | Model file size |
|---|---:|---:|---:|
| VGG16 | 92 | 89 | 367 |
| ResNet50 | 76 | 98 | 407 |
| MobileNetV2 | 55 | 77 | 325 |

![image](https://user-images.githubusercontent.com/61040406/91663207-6be7f300-eb22-11ea-8ccf-6b0449a0b6bb.png)

 MobileNetV2는 한 에폭 당 학습 시간이 가장 빨랐습니다. 모델은 같은 성능을 낼 때 단순할수록 좋습니다([오컴의 면도날](https://en.wikipedia.org/wiki/Occam%27s_razor)). MobileNetV2는 성능이 가장 우수하면서도 parameter 개수는 가장 적었습니다. 실시간으로 학습자의 수업 참여도를 예측하는 우리의 시스템은 학습된 모델의 파일 크기가 작을수록 좋습니다. MobileNetV2로 학습된 모델의 파일 크기가 가장 작았습니다.

# Installing

```python
$ pip install tensorflow
$ pip install scikit-learn
```

# Repository

```
└── Model
        ├── constants.py
        ├── data_generator.py
        ├── data_utils.py
        ├── json_to_df.py
        ├── main.py
        ├── model.py
```

1. constants.py

    : 학습 전 이미지 크기, 모델 이름 등 인자 설정

2. data_generator.py

    : 데이터셋 생성

3. data_utils.py

    : 인풋 이미지와 벡터 전처리

4. json_to_df.py

    : 전체 분석 과정에서 사용하기 위해 json 파일로부터 dataframe 생성

5. main.py

    : 모델 학습

6. model.py

    : 모델 구조 정의

# References

- [[Karen Simonyan 2014](https://papers.nips.cc/paper/5353-two-stream-convolutional-networks-for-action-recognition-in-videos)] Two-Stream Convolutional Networks for Action Recognition in Videos
- [[Karen Simonyan 2014](https://arxiv.org/abs/1409.1556)] Very Deep Convolutional Networks for Large-Scale Image Recognition
- [[Yaniv Taigman 2014](https://www.cv-foundation.org/openaccess/content_cvpr_2014/html/Taigman_DeepFace_Closing_the_2014_CVPR_paper.html)] DeepFace: Closing the Gap to Human-Level Performance in Face Verification
- [[Yusuke Sugano 2014](https://ieeexplore.ieee.org/document/6909631)] Learning-by-Synthesis for Appearance-based 3D Gaze Estimation
- [[Kaiming He 2015](https://arxiv.org/abs/1512.03385)] Deep Residual Learning for Image Recognition
- [[Zhang 2015](https://arxiv.org/abs/1504.02863)] Appearance-Based Gaze Estimation in the Wild
- [[Christoph Feichtenhofer 2016](https://arxiv.org/abs/1604.06573)] Convolutional Two-Stream Network Fusion for Video Action Recognition
- [[Kyle Krafka 2016](https://arxiv.org/abs/1606.05814)] Eye Tracking for Everyone
- [[Xucong Zhang 2016](https://arxiv.org/abs/1611.08860)] It's Written All Over Your Face: Full-Face Appearance-Based Gaze Estimation
- [[Haoping Deng 2017](https://ieeexplore.ieee.org/document/8237603)] Monocular Free-Head 3D Gaze Tracking with Deep Learning and Geometry Constraints
- [[Cristina Palmero 2018](https://arxiv.org/abs/1805.03064)] Recurrent CNN for 3D Gaze Estimation using Appearance and Shape Cues
- [[Mark Sandler 2018](https://arxiv.org/abs/1801.04381)] MobileNetV2: Inverted Residuals and Linear Bottlenecks
