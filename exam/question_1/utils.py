
###########
# Imports #
###########
# Type hints
from typing import Literal
from typing import Optional

import tensorflow as tf
from keras import layers

# data
import pandas as pd
import numpy as np
import tensorflow_datasets  as tfds

# Plotting
import matplotlib.pyplot as plt

########
# Data #
########
# ----- Helper functions -----
def _convert_sample(sample: pd.DataFrame,
                    gray_scale: bool = False,
                    size: tuple[int, int] | None = None) -> tuple[np.ndarray, np.ndarray]:
    '''
    Desc
    -----
    Convert the pandas DataFrame into a list of images and a list of one hot encoding labels
    The Images can also be converted to gray_scale and resized if necessary
    
    Return
    -------
    pandas (images)
    list of numpy arrays (labels)
    '''
    # Get data
    image, label = sample['image'], sample['label']  
    image = tf.image.convert_image_dtype(image, tf.float32)
    label = tf.one_hot(label, 2, dtype=tf.float32)
    return image, label


def load_data(data_dir: str,
              perc: int = 5,
              batch_size: int = 32) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''
    Desc
    -----
    Returns a tuple of the train, test and validation data in a 80% 10% 10%
    
    Params
    -------
    data_dir: The path to the data directory
    perc: the percentage of the full data
    
    Return
    -------
    Tuple of numparrays
    '''
    # Load data set
    train_df, test_df, val_df = tfds.load('patch_camelyon',split=[f'train[:{perc}%]', f'test[:{perc}%]', f'validation[:{perc}%]'],
                                          data_dir = data_dir,
                                          download=False,
                                          shuffle_files=True)
    
    train_dataset = train_df.map(_convert_sample).batch(batch_size)
    test_dataset = test_df.map(_convert_sample).batch(batch_size)
    validation_dataset = val_df.map(_convert_sample).batch(batch_size)
    return train_dataset, test_dataset, validation_dataset

#####################
# Data augmentation #
#####################
def augment_layer(size: Optional[int] = None,
                 flip: Optional[Literal["horizontal_and_vertical", "horizontal", "vertical"]] = None,
                 rotation: Optional[float] = None,
                 zoom: Optional[tuple[float, float]] = None,
                 contrast: Optional[float] = None,
                 brightness: Optional[float] = None) -> layers:
    """
    Description
    ------------
    An augmentation layers for the images
    If any parameters is left out, this particular augmentation will not be performed
    
    Parameters
    ----------
    - size (integer or None): Size of new image
    - flip (str: 'horizontal_and_vertical', 'horizontal', 'vertical' or None): How to flip the image
    - rotation (float or None): How many percentage degrees to rotate the image
    - zoom (tuple(float, float) or None): How much to zoom the picture in height and width as a percentage
    - contrast (float or None): How much contrast to add to each picture
    - brightness (float or None): How much brightness to add between -1 (black) and 1 (white)

    Returns
    -------
    - returns a keras layer
    """
    aug_layers = []
    if size is not None:
        aug_layers.append(layers.Resizing(size, size))
    if flip is not None:
        aug_layers.append(layers.RandomFlip(flip))
    if rotation is not None:
        aug_layers.append(layers.RandomRotation(rotation))
    if zoom is not None:
        aug_layers.append(layers.RandomZoom(rotation))
    if contrast is not None:
        aug_layers.append(layers.RandomContrast(contrast))
    if brightness is not None:
        aug_layers.append(layers.RandomBrightness(rotation))
    return tf.keras.Sequential(aug_layers)
  
  
   
############
# Plotting #
############
def plot_hist(history):
    '''
    Desc
    -----
    Plots the accuracy and loss for training and validation data
    Stacks them on
    '''
    
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(acc) + 1)

    figure, axis = plt.subplots(2, 1) # display two plots in one graph

    axis[0].plot(epochs, acc, label='Training accuracy')
    axis[0].plot(epochs, val_acc, label='Validation accuracy')
    axis[0].set_title('Training and validation accuracy')
    plt.legend()

    axis[1].plot(epochs, loss, label='Training loss')
    axis[1].plot(epochs, val_loss, label='Validation loss')
    axis[1].set_title('Training and validation loss')
    plt.legend()

    plt.show()


def plot_hist_sideways(history):
    """
    Plots loss and accuracy side by side
    """
    history_dict = history.history


    # Plot 1 values
    loss_values = history_dict['loss']
    val_loss_values = history_dict['val_loss']


    # Plot 2 values
    acc_values = history_dict['accuracy']
    val_values = history_dict['val_accuracy']

    epochs = range(1, len(loss_values) + 1)


    # Plot 1
    plt.subplot(1,2,1)
    plt.plot(epochs, loss_values, 'r', label='Training loss') # 'bo' is for blue dot, 'b' is for solid blue line
    plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()


    # Plot 2
    plt.subplot(1,2,2)
    plt.plot(epochs, acc_values, 'r', label='Training accuracy')
    plt.plot(epochs, val_values, 'b', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.show()