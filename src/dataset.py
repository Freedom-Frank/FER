import csv
import numpy as np
import pandas as pd
import cv2
from pathlib import Path


class FER2013Dataset:
    """FER2013数据集加载器，支持数据增强和Mixup"""
    def __init__(self, csv_path, usage='Training', augment=False, mixup=False, mixup_alpha=0.2):
        self.data = pd.read_csv(csv_path)
        self.usage = usage
        self.augment = augment  # 是否使用数据增强
        self.mixup = mixup  # 是否使用Mixup
        self.mixup_alpha = mixup_alpha  # Mixup的alpha参数

        if usage == 'Training':
            self.data = self.data[self.data['Usage'] == 'Training']
        elif usage == 'PublicTest':
            self.data = self.data[self.data['Usage'] == 'PublicTest']
        elif usage == 'PrivateTest':
            self.data = self.data[self.data['Usage'] == 'PrivateTest']

        # 重置索引以避免索引问题
        self.data = self.data.reset_index(drop=True)

    def __getitem__(self, index):
        row = self.data.iloc[index]
        img_str = row['pixels']
        # 修复废弃警告: 使用 np.fromstring 改为推荐的方法
        img_array = np.array([float(x) for x in img_str.split()], dtype=np.float32).reshape(48, 48)

        # 数据增强 (仅在训练时)
        if self.augment:
            img_array = self._augment(img_array)

        # Mixup增强（在数据加载时混合）
        if self.mixup and self.usage == 'Training':
            # 随机选择另一个样本
            mix_index = np.random.randint(0, len(self.data))
            mix_row = self.data.iloc[mix_index]
            mix_img_str = mix_row['pixels']
            mix_img_array = np.array([float(x) for x in mix_img_str.split()], dtype=np.float32).reshape(48, 48)

            if self.augment:
                mix_img_array = self._augment(mix_img_array)

            # Mixup lambda
            lam = np.random.beta(self.mixup_alpha, self.mixup_alpha)
            img_array = lam * img_array + (1 - lam) * mix_img_array

            # 使用软标签：返回one-hot混合标签
            label_a = row['emotion']
            label_b = mix_row['emotion']

            # 创建混合的one-hot标签
            mixed_label = np.zeros(7, dtype=np.float32)
            mixed_label[label_a] = lam
            mixed_label[label_b] += (1 - lam)

            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)  # (1,48,48)
            pixels = np.asarray(img_array, dtype=np.float32)

            # 返回格式：(image, soft_label) - 软标签作为float数组
            return pixels, mixed_label

        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # (1,48,48)

        pixels = np.asarray(img_array, dtype=np.float32)
        label = np.asarray(row['emotion'], dtype=np.int32)
        return pixels, label

    def _augment(self, img):
        """增强的数据增强：随机水平翻转、旋转、亮度、对比度、噪声、平移"""
        # 随机水平翻转 (50%概率)
        if np.random.rand() > 0.5:
            img = np.fliplr(img)

        # 随机旋转 (-20度到20度，增加范围)
        if np.random.rand() > 0.5:
            angle = np.random.uniform(-20, 20)
            h, w = img.shape
            M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
            img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

        # 随机亮度调整 (±30%，增加范围)
        if np.random.rand() > 0.5:
            brightness_factor = np.random.uniform(0.7, 1.3)
            img = np.clip(img * brightness_factor, 0, 255)

        # 随机对比度调整（新增）
        if np.random.rand() > 0.5:
            alpha = np.random.uniform(0.8, 1.2)  # 对比度因子
            img = np.clip(128 + alpha * (img - 128), 0, 255)

        # 随机高斯噪声（新增，小概率）
        if np.random.rand() > 0.7:
            noise = np.random.normal(0, 3, img.shape)
            img = np.clip(img + noise, 0, 255)

        # 随机平移（新增，±10%）
        if np.random.rand() > 0.5:
            h, w = img.shape
            tx = np.random.uniform(-0.1, 0.1) * w
            ty = np.random.uniform(-0.1, 0.1) * h
            M = np.float32([[1, 0, tx], [0, 1, ty]])
            img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

        # 随机擦除（Cutout，新增，小概率）
        if np.random.rand() > 0.8:
            h, w = img.shape
            mask_size = int(min(h, w) * 0.15)  # 擦除区域15%
            x = np.random.randint(0, w - mask_size)
            y = np.random.randint(0, h - mask_size)
            img[y:y+mask_size, x:x+mask_size] = np.mean(img)

        return img



    def __len__(self):
        return len(self.data)




# helper to create MindSpore GeneratorDataset in train script
# (placed here so train.py 只需 import)