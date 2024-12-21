# Metrics Library

This library provides utilities for calculating various metrics in image quality assessment and classification.

## Features
- Image Quality Metrics: PSNR, SSIM, MSE, FID, NIQE
- Classification Metrics: Confusion Matrix, Accuracy, Precision, Recall, F1 Score

## Installation
```bash
pip install mmetrics
```

## Usage
```python
'''Image Quality Assessment'''
from metrics.image_quality import psnr, ssim, mse, niqe, fid

#Load your images to compare using any tool to have them as numpy arrays
psnr(img1, img2)
ssim(img1, img2)
mse(img1, img2)
niqe(img1)

#Put the path of your images
fid(real_images_path, fake_images_path)

'''Classification Assessment'''
from metrics.classification import confusion_matrix, accuracy, precision, recall, f1_score, jaccard_index

#Load your ground truth (y_true) and your predictions (y_pred) as numpy arrays 
confusion_matrix(y_true, y_pred)
accuracy(y_true, y_pred)
precision(y_true, y_pred)
recall(y_true, y_pred)
f1_score(y_true, y_pred)
jaccard_index(y_true, y_pred)

```