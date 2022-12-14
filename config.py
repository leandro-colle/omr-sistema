import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import sys
import json
import cv2 as cv
import numpy as np
import tensorflow as tf
from midiutil import MIDIFile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))