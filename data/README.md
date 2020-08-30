# Data Features

### Face and Eye image

1. landmark 검출 후 얼굴, 왼쪽 눈, 오른쪽 눈 각각 crop
    - landmark 검출 시 pre-trained model([shape_predictor_68_face_landmarks.dat](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)) 사용
2. Face는 (154, 154, 3) Eye는 (224, 224, 3)로 resize 후 jpg파일로 저장

<img src="https://user-images.githubusercontent.com/43233184/91655583-9c149f00-eaec-11ea-9b8d-50f469c647b9.png" width="550px">

### Headpose

1. 원리
<img src="https://user-images.githubusercontent.com/43233184/91655590-aa62bb00-eaec-11ea-8a0e-faec947e75e6.png" width="500">
<img src="https://user-images.githubusercontent.com/43233184/91655593-afc00580-eaec-11ea-945d-54e9f4f5ff21.png" width="300">
<img src="https://user-images.githubusercontent.com/43233184/91655597-b2225f80-eaec-11ea-9732-5df31ee66176.png" width="300">


- 우리가 알고 있는 좌표인 World coordination, Image plane coordination, Camera coordination을 이용해 Rotation value 검출하는 원리를 이용

2. 값 추출

- [github open api](https://github.com/qhan1028/Headpose-Detection) 이용해 Rotation value인 pitch-yaw-roll(Euler angles) 값 추출


<img src="https://user-images.githubusercontent.com/43233184/91655601-b9e20400-eaec-11ea-80ae-e31bef55f7ee.png" width="300">

# Data EDA

### Dataframe Structure

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 13563 entries, 0 to 13562
Data columns (total 10 columns):
 #   Column            Non-Null Count  Dtype  
---  ------            --------------  -----  
 0   frame_name        13563 non-null  object 
 1   subject           13563 non-null  object 
 2   head_pose_pitch   13563 non-null  float64
 3   head_pose_yaw     13563 non-null  float64
 4   head_pose_roll    13563 non-null  float64
 5   face_landmarks    13563 non-null  object 
 6   faceimg_name      13563 non-null  object 
 7   lefteyeimg_name   13563 non-null  object 
 8   righteyeimg_name  13563 non-null  object 
 9   label             13563 non-null  object 
dtypes: float64(3), object(7)
memory usage: 1.0+ MB
```

### Number of data per Subjects

<p align="center"><img src="https://user-images.githubusercontent.com/43233184/91655608-bfd7e500-eaec-11ea-92c3-6cdb6859c550.png"></p>

### Number of data per label
<p align="center"><img src="https://user-images.githubusercontent.com/43233184/91655612-c23a3f00-eaec-11ea-9331-f461c35870ff.png"></p>

- label 0(41.92%) : 온라인 수업 **화면이 아닌 곳을 응시**
- label 1(58.08%) : 온라인 수업 **화면 응시**

### Correlation of Headpose

#### Heatmap
<p align="center"><img src="https://user-images.githubusercontent.com/43233184/91655614-c5352f80-eaec-11ea-94cb-2b4df370cb62.png" width="90%"></p>

<p align="center"><img src="https://user-images.githubusercontent.com/43233184/91655617-c7978980-eaec-11ea-8add-b4da5af999b3.png"></p>

### Distribution of Headpose

#### violin plot
<p align="center"><img src="https://user-images.githubusercontent.com/43233184/91655618-cb2b1080-eaec-11ea-9b51-c1130febaa4b.png" width="90%"></p>


# Make metadata

## Installing

Install and update using pip:

```python
# opencv
$ pip install opencv-python

# dlib
$ pip install cmake
$ pip install dlib 
```

## Repository

```
└── preprocessing
        ├── cut_eyelm.py
        ├── cut_facelm.py
        ├── generate_data.py
        ├── headpose.py
        ├── json_to_df.py
        ├── timer.py
        ├── utils.py
└── EDA.ipynb
```

1. preprocessing
    - 데이터 전처리 및 데이터 저장을 위한 json 파일 생성 폴더
2. EDA.ipynb
    - EDA 및 유의성 검정

## Run

### before run

```python
# generate_data.py

20    video_dir = 'C:/Users/sodaus/Desktop/data/ver3456final/video/' #path of video dir

26    img_dir = 'C:/Users/sodaus/Desktop/data/ver3456final/img/'

126   # metadata 저장을 위한 json 파일 생성 
127   datadict = {}
128   datadict['data'] = data 
129   json.dumps(datadict, ensure_ascii=False, indent="\t")
130   with open('your path and your json file name', 'w', encoding="utf-8") as make_file:
131      json.dump(datadict, make_file, ensure_ascii=False, indent='\t')
```

1. line 20
    - raw_data로 사용할 video가 있는 directory path로 변경
2. line 26
    - 이미지를 저장할 directory로 path를 변경
3. line 130
    - json을 저장할 path와 json명 설정

### to make json file

```python
$ python preprocessing/generate_data.py
```

### to make json file to pandas dataframe

```python
$ python preprocessing/json_to_df.py
```

## References

- [https://github.com/qhan1028/Headpose-Detection](https://github.com/qhan1028/Headpose-Detection)
- [https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib](https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib) - headpose 원리
