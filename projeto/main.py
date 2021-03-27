import cv2
import math
from pyzbar import pyzbar

def read_image(path):
  return cv2.imread(path)

def decode_image(image):
  return pyzbar.decode(image)

def get_image_properties(image):
  height = image.shape[0]
  width = image.shape[1]

  return (height, width)

def correct_image_orientation(image):

def split_image_in_half(image):
  (height, width) = get_image_properties(image)
  first_half = image[0:math.floor(height/2), :]
  second_half = image[math.floor(height/2):, :]

  return (first_half, second_half)

def get_barcodes(image):
  data = None
  decoded = decode_image(image)
  
  for barcode in decoded:
    data = barcode.data.decode("utf-8")

  return data

def procces_image(path, output_path):
  image = read_image(path)
  cv2.imwrite(output_path, image)
  (first_half, second_half) = split_image_in_half(image)
  first_barcode = get_barcodes(first_half)
  second_barcode = get_barcodes(second_half)
  print("aaaa", first_barcode, second_barcode)

procces_image("D04Q1I1802200012.jpg", "test.png")