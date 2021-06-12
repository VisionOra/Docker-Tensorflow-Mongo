import numpy as np
import tensorflow as tf


DIV2K_RGB_MEAN = np.array([0.4488, 0.4371, 0.4040]) * 255


def resolve_single(model, lr):
    return resolve(model, tf.expand_dims(lr, axis=0))[0]


def resolve(model, lr_batch):
    lr_batch = tf.cast(lr_batch, tf.float32)
    sr_batch = model(lr_batch)
    sr_batch = tf.clip_by_value(sr_batch, 0, 255)
    sr_batch = tf.round(sr_batch)
    sr_batch = tf.cast(sr_batch, tf.uint8)
    return sr_batch


def cal_scores(model, lr, hr):
    sr = resolve(model, lr)
    return psnr(hr, sr)[0], ssim(hr, sr)[0]

def evaluate(model, train_dataset, val_dataset):
    train_psnr_values, train_ssim_values, val_psnr_values, val_ssim_values = [], [], [], []
    for (train_lr, train_hr), (val_lr, val_hr) in zip(train_dataset, val_dataset):
        
        # Training Evaluation
        train_psnr_value, train_ssim_value =  cal_scores(model, train_lr, train_hr)
        train_psnr_values.append(train_psnr_value); train_ssim_values.append(train_ssim_value)
        
        # Validation Evaluation 
        val_psnr_value, val_ssim_value =  cal_scores(model, val_lr, val_hr)
        val_psnr_values.append(val_psnr_value); val_ssim_values.append(val_ssim_value)
        
    
    return [tf.reduce_mean(train_psnr_values), tf.reduce_mean(train_ssim_values), tf.reduce_mean(val_psnr_values), tf.reduce_mean(val_ssim_values)]


# ---------------------------------------
#  Normalization
# ---------------------------------------


def normalize(x, rgb_mean=DIV2K_RGB_MEAN):
    return (x - rgb_mean) / 127.5


def denormalize(x, rgb_mean=DIV2K_RGB_MEAN):
    return x * 127.5 + rgb_mean


def normalize_01(x):
    """Normalizes RGB images to [0, 1]."""
    return x / 255.0


def normalize_m11(x):
    """Normalizes RGB images to [-1, 1]."""
    return x / 127.5 - 1


def denormalize_m11(x):
    """Inverse of normalize_m11."""
    return (x + 1) * 127.5


# ---------------------------------------
#  Metrics
# ---------------------------------------


def psnr(x1, x2):
    return tf.image.psnr(x1, x2, max_val=255)

def ssim(x1, x2):
    return tf.image.ssim(x1, x2, max_val = 255)


# ---------------------------------------
#  See https://arxiv.org/abs/1609.05158
# ---------------------------------------


def pixel_shuffle(scale):
    return lambda x: tf.nn.depth_to_space(x, scale)


