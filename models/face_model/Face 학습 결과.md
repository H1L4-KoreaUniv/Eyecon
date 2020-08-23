# Face 학습 결과

# 1. LJW_face_weights1.h5

## Info

- Data: ver3-2 - LDH, LJW, HYJ
    - 약 19,000장
    - train: 0.8, valid: 0.2
    - batch = 32
    - shuffle = True
- Augmentation:
    - Resize(224), Rescale(/255.0)  # Aug라기에는..?
    - RandomHorizontalFlip
    - RandomBrightness(max_delta=0.15)
    - RandomContrast(0.7, 1.3)
    - RandomHue(0.05) # 색조
    - RandomSaturation(0.7, 2.0) # 채도
    - GaussianNoise(0.08)
- Model: VGG16
    - weights: pre-trained with Imagenet
        - train layers: fc6, fc7 = 2048, 2048 with Dropout(0.5)
- Compile:
    - optim = Adam(lr=0.001)
    - loss = Binary crossentropy
- Pipeline:
    1. load data, batch, shuffle, train_valid_split, seed=112
    2. cache
    3. augmentation
    4. prefetch
    5. train
- Train:
    - epochs = 10
    - early_stop: patience = 5

## Result

![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled.png)

![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%201.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%201.png)

Prediction:

- prediction with unseen data(seen person)

    ![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%202.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%202.png)

- prediction with unseen data(unseen person)

    BAD result ← accuracy: 0.3126

## Knowledge?

- 처음 본 사람은 많이 틀리지만, 봤던 사람은 학습하지 않은 새로운 이미지도 잘 맞힌다.

# 2. Not_saved.h5

## Info

- Data: ver3-2 - LDH, LJW, HYJ
    - 약 19,000장
    - train: 0.8, valid: 0.2
    - batch = 64
    - shuffle = True
- Augmentation: No
    - Resize(224), Resclae(/255.0)  # Aug라기에는..?
- Model: VGG16
    - weights: pre-trained with Imagenet
        - train layers: fc6, fc7 = 2048, 2048 with Dropout(0.5)
- Compile:
    - optim = Adam(lr=0.001)
    - loss = Binary crossentropy
- Pipeline:
    1. load data, batch, shuffle, train_valid_split, seed=112
    2. cache
    3. ~~augmentation~~
    4. prefetch
    5. train
- Train:
    - epochs = 10
    - early_stop: patience = 5

## Result

![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%203.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%203.png)

![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%204.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%204.png)

Prediction:

- prediction with unseen data(seen person)

    ![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%205.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%205.png)

- prediction with unseen data(unseen person)

    해보나 마나.

## Knowledge?

- Augmentation 안 해주니 봤던 사람이라도 학습하지 않은 새로운 이미지 잘 못 맞힌다.
- time, resource issue: VGG16 기준
    - 배치 작든 크든 학습 시간이 거의 비슷하다. 원래 작으면 빨라지는 관계인데.
    - cache()로 에폭당 6초 정도 줄인다.
    - Augmentation 하는데 에폭 안에서 2초 걸린다.
    - prefetch()로 에폭당 2초 정도 줄인다.
    - 학습할 때만 CPU 80% 사용하고, val에서는 사용하지 않는다.

# 3. LJW_face_weights2.h5

## Info

- Data: ver3-2 - LDH, LJW, HYJ
    - 약 19,000장
    - train: 0.8, valid: 0.2
    - batch = 128
    - shuffle = True
- Augmentation:
    - Resize(224), Resclae(/255.0)  # Aug라기에는..?
    - RandomHorizontalFlip
    - RandomBrightness(max_delta=0.15)
    - RandomContrast(0.7, 1.3)
    - RandomHue(0.05) # 색조
    - RandomSaturation(0.7, 2.0) # 채도
    - GaussianNoise(0.08)
- Model: MobileNetV2
    - weights: pre-trained with Imagenet
        - train layers: fc = 1 (trainable parameter 1281)
- Compile:
    - optim = Adam(lr=0.001)
    - loss = Binary crossentropy
- Pipeline:
    1. load data, batch, shuffle, train_valid_split, seed=112
    2. cache
    3. augmentation
    4. prefetch
    5. train
- Train:
    - epochs = 30
    - early_stop: patience = 5

## Result

![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%206.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%206.png)

![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%207.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%207.png)

Prediction:

- prediction with unseen data(seen person)

    ![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%208.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%208.png)

- prediction with unseen data(unseen person)

    ![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%209.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%209.png)

## Knowledge?

- time, resource issue: MobileNetV2기준
    - 첫 에폭 79초, 나머지와 1분 차이!
- 모바일넷은 처음 본 사람도 맞힌다.

# 4. LJW_face_weights3.h5

## Info

- Data: ver3-2 - LDH, LJW, HYJ, LSH, KSG, JHW, UTH
    - 약 24,000장
    - train: 0.8, valid: 0.2
    - batch = 128
    - shuffle = True
- Augmentation:
    - Resize(224), Rescale(/255.0)  # Aug라기에는..?
    - RandomHorizontalFlip
    - RandomBrightness(max_delta=0.15)
    - RandomContrast(0.7, 1.3)
    - RandomHue(0.05) # 색조
    - RandomSaturation(0.7, 2.0) # 채도
    - GaussianNoise(0.08)
- Model: MobileNetV2
    - weights: pre-trained with Imagenet
        - train layers: fc = 1 (trainable parameter 1281)
- Compile:
    - optim = Adam(lr=0.001)
    - loss = Binary crossentropy
- Pipeline:
    1. load data, batch, shuffle, train_valid_split, seed=112
    2. cache
    3. augmentation
    4. prefetch
    5. train
- Train:
    - epochs = 30
    - early_stop: patience = 5

## Result

![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%2010.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%2010.png)

![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%2011.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%2011.png)

Prediction:

- prediction with unseen data(seen person)

    ![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%2012.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%2012.png)

- prediction with unseen data(unseen person)

    ![Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%2013.png](Face%20%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%B3%E1%86%B8%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%202cb306e754ce46ed8790a87b0c5a5d5e/Untitled%2013.png)

## Knowledge?

- time, resource issue: MobileNetV2기준
    - 첫 에폭과 나머지 2분 차이. 병렬의 힘은 데이터가 커질수록 느껴진다.
- 이번에는 봤던 사람은 못 맞히고, 못 봤던 사람은 잘 맞힌다.