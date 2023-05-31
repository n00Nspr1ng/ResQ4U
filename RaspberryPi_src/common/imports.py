#!/usr/bin/env python3
# IMPORTS
import argparse
import cv2
import os

from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference

import serial
import time
import config

import RPi.GPIO as GPIO

from twilio.rest import Client # for calling
