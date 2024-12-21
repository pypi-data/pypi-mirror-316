import numpy as np
from skimage.metrics import structural_similarity, peak_signal_noise_ratio,mean_squared_error
from skimage import img_as_float
from pytorch_fid import fid_score
import torch
from torchvision.models import inception_v3
from torchvision import transforms
from PIL import Image
from scipy.linalg import sqrtm


def psnr(img1, img2):
    """
    Calculate PSNR between two images of the same dimensions.

    Args:
        img1: numpy array, first image
        img2: numpy array, second image

    Returns:
        PSNR value in dB
    """
    # Ensure the images have the same shape
    if img1.shape != img2.shape:
        raise ValueError("Input images must have the same dimensions.")
    
    # Compute Mean Squared Error (MSE)
    mse = np.mean((img1.astype(float) - img2.astype(float) ) ** 2)
    if mse == 0:
        return float('inf')  # Return infinity if images are identical
    
    # Determine max pixel value based on data type
    if np.issubdtype(img1.dtype, np.integer):
        max_pixel = np.iinfo(img1.dtype).max  # Maximum value for integer types
    elif np.issubdtype(img1.dtype, np.floating):
        max_pixel = 1.0  # For normalized floats (assume [0, 1])
    else:
        raise ValueError("Unsupported image data type.")
    
    # Compute PSNR
    psnr_value = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr_value   

def ssim(img1,img2):
    """
    Calculate SSIM between two images using the SSIM formula.

    Args:
        img1: numpy array, first image
        img2: numpy array, second image

    Returns:
        SSIM value
    """
    # Ensure the images have the same shape
    if img1.shape != img2.shape:
        raise ValueError("Input images must have the same dimensions.")
    
    # Determine max pixel value based on data type
    if np.issubdtype(img1.dtype, np.integer):
        max_pixel = np.iinfo(img1.dtype).max  # Maximum value for integer types
    elif np.issubdtype(img1.dtype, np.floating):
        max_pixel = 1.0  # For normalized floats (assume [0, 1])
    else:
        raise ValueError("Unsupported image data type.")
    
    # Constants for numerical stability
    C1 = (0.01 * max_pixel) ** 2
    C2 = (0.03 * max_pixel) ** 2

    # Means
    mu_x = np.mean(img1.astype(float))
    mu_y = np.mean(img2.astype(float))

    # Variances and covariance
    sigma_x = np.var(img1.astype(float))
    sigma_y = np.var(img2.astype(float))
    sigma_xy = np.mean((img1.astype(float) - mu_x) * (img2.astype(float) - mu_y))

    # SSIM formula
    numerator = (2 * mu_x * mu_y + C1) * (2 * sigma_xy + C2)
    denominator = (mu_x ** 2 + mu_y ** 2 + C1) * (sigma_x + sigma_y + C2)
    ssim_value = numerator / denominator

    return ssim_value

def mse(img1,img2):
    """Returns the Mean Squared Error between two images"""
    return np.mean((img1.astype(float) - img2.astype(float))**2)

def fid(real_images_path, fake_images_path):
    """
    Calculate FID between two sets of images using their file paths.

    Args:
        real_image_paths: List of file paths to real images.
        generated_image_paths: List of file paths to generated images.

    Returns:
        FID value (float).
    """
    # Load pre-trained Inception-v3 model
    model = inception_v3(pretrained=True, transform_input=False)
    model.fc = torch.nn.Identity()  # Remove the final classification layer
    model.eval()

    # Transformation for input images (resize, normalize, etc.)
    transform = transforms.Compose([
        transforms.Resize((299, 299)),  # Required for Inception-v3
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    def extract_features(image_paths, model):
        """
        Extract features from images using a pre-trained model.
        
        Args:
            image_paths: List of file paths to images.
            model: Pre-trained model for feature extraction.
        
        Returns:
            Numpy array of extracted features, shape (N, 2048).
        """
        features = []
        with torch.no_grad():
            for path in image_paths:
                try:
                    image = Image.open(path).convert("RGB")
                    input_tensor = transform(image).unsqueeze(0)  # Add batch dimension
                    feature = model(input_tensor).squeeze(0).numpy()  # Remove batch dimension
                    features.append(feature)
                except Exception as e:
                    print(f"Error processing image {path}: {e}")
        return np.array(features)

    # Extract features for real and generated images
    print("Extracting features for real images...")
    real_features = extract_features(real_images_path, model)

    print("Extracting features for generated images...")
    generated_features = extract_features(fake_images_path, model)

    # Ensure features are valid
    if real_features.shape[0] == 0 or generated_features.shape[0] == 0:
        raise ValueError("Feature extraction failed. Ensure the input image paths are valid.")

    # Calculate FID
    def calculate_fid(real_features, generated_features):
        # Mean and covariance of real and generated features
        mu_r = np.mean(real_features, axis=0)
        mu_g = np.mean(generated_features, axis=0)
        sigma_r = np.cov(real_features, rowvar=False)
        sigma_g = np.cov(generated_features, rowvar=False)

        # Mean difference squared
        mean_diff = mu_r - mu_g
        mean_diff_squared = np.sum(mean_diff ** 2)

        # Trace term for covariance matrices
        cov_mean = sqrtm(sigma_r @ sigma_g)  # Matrix square root of product of covariances
        # Handle numerical errors
        if np.iscomplexobj(cov_mean):
            cov_mean = cov_mean.real

        trace_term = np.trace(sigma_r + sigma_g - 2 * cov_mean)

        return mean_diff_squared + trace_term

    # Compute and return FID
    fid_value = calculate_fid(real_features, generated_features)
    return fid_value

def niqe(img):
    """Returns the Natural Image Quality Evaluator of a artificially generated image"""
    img = img_as_float(img)
    return mse(img, np.zeros_like(img))  # Example using MSE as a placeholder


