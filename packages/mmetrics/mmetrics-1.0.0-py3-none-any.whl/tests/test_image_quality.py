import numpy as np
from metrics.image_quality import psnr, ssim, mse, niqe, fid
from skimage.metrics import peak_signal_noise_ratio as psnrr, structural_similarity as ssimm

def test_psnr():
    img1 = np.ones((256, 256), dtype=np.uint8) * 255
    img2 = np.ones((256, 256), dtype=np.uint8)
    print(psnr(img1, img2))
    print(psnrr(img1, img2))
    print("##########")

def test_ssim():
    img1 = np.ones((256, 256), dtype=np.uint8)
    img2 = np.ones((256, 256), dtype=np.uint8)
    print(ssim(img1, img2))
    print(ssimm(img1,img2))
    print("##########")

def test_mse():
    img1 = np.ones((256, 256), dtype=np.uint8)
    img2 = np.ones((256, 256), dtype=np.uint8)
    print(mse(img1, img2))
    print("##########")

def test_niqe():
    img1 = np.ones((256, 256), dtype=np.uint8)
    print(niqe(img1))
    print("##########")

test_psnr()
test_ssim()
test_mse()
test_niqe()