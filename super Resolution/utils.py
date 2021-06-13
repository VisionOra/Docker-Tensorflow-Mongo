import matplotlib.pyplot as plt
import tensorflow as tf
# physical_devices = tf.config.list_physical_devices('GPU') 
# for gpu_instance in physical_devices: 
#     tf.config.experimental.set_memory_growth(gpu_instance, True)

# from tensorflow.compat.v1.keras.backend import set_session
# config = tf.compat.v1.ConfigProto()
# config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
# config.log_device_placement = True  # to log device placement (on which device the operation ran)
# sess = tf.compat.v1.Session(config=config)
# set_session(sess)



import os
import matplotlib.pyplot as plt
from data import DIV2K
from model.srgan import generator, discriminator
from train import SrganTrainer, SrganGeneratorTrainer
from model.common import resolve_single


# Location of model weights (needed for demo)
weights_dir = 'weights/srgan_4x'
weights_file = lambda filename: os.path.join(weights_dir, filename)
os.makedirs(weights_dir, exist_ok=True)

# Loading a pretrained Model
pre_generator = generator()
pre_generator.load_weights(weights_file('pre_generator.h5'))




from PIL import Image
import io
import numpy as np


def conversion(img):
    '''
    Description:
        Convert base64 image to PIL and PIL image to base 64
    '''
    
    def base64_conversion(img: Image.Image ) -> str:
        '''
            Description:
                This fucntion helps you to convert PIL image to a base64 image.

            Input:
                PIL_IMG (PIL): PIL Image Object

            Output:
                base64_img (str) : Base64 of the image
        '''


        # Converting Image to baes64
        image_bytes = io.BytesIO()
        img.save(image_bytes, format='JPEG')
        return image_bytes.getvalue()

    def PIL_conversion(img : str) -> Image.Image:
        '''
            Description:
                This fucntion helps you to convert base64 image to a PIL image.

            Input:
                base64_img (str) : Base64 of the image

            Output:
                PIL_IMG (PIL): PIL Image Object
        '''

        # Converting the base64 image back to Pil object.
        pil_img = Image.open(io.BytesIO(img))

        # Displaying Image
        return pil_img
    
    if isinstance(img, (bytes)):
        return PIL_conversion(img)
    
    elif isinstance(img, (Image.Image)):
        return base64_conversion(img)
    
    else:
        raise ValueError('Wrong parameter passed to the fucntion. Only PIL and Bytes object is supported')
        return 0
    
    

    
def predict(image):
    '''
        Description:
            This function will get the predictions of the model and return a byte object of super resolution model

        Input:
            image (PIL, Nd.array, bytes): Image

        Output:
            sr (bytes) : super resolution of the model
    
    '''
    
    # Converting to PIL object if its a byte object
    if isinstance(image, (bytes)): image = np.asarray(conversion(image))
    
    # Prediction super resolution of the image
    with tf.device('/cpu:0'):
        sr = resolve_single(pre_generator, image)
    
    # Converting Nd array -> PIL -> Bytes
    sr = conversion(Image.fromarray(sr.numpy()))
    
    # Return
    return sr


        
        


        
        