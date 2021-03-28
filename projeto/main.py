import cv2
import math
from pyzbar import pyzbar
import numpy as np

def read_image(path):
  return cv2.imread(path)

def write_image(path, image):
  return cv2.imwrite(path, image)

def decode_image(image):
  return pyzbar.decode(image)

def get_image_properties(image):
  height = image.shape[0]
  width = image.shape[1]

  return (height, width)

def convert_image_to_grayscale(image):
  return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def get_grayscale_histogram(image):
  data = {}
  grayscale = convert_image_to_grayscale(image)
  (height, width) = get_image_properties(grayscale)

  for i in range(height):
    for j in range(width):
      key = grayscale[i][j]
      if(key in data):
        data[key] += 1
      else:
        data[key] = 1
  return data

def split_image_in_half(image):
  (height, _) = get_image_properties(image)
  fraction = math.floor(height/2)

  first_half = image[0:fraction, :]
  second_half = image[fraction:, :]

  return (first_half, second_half)

def split_image_in_thirds(image):
  (_, width) = get_image_properties(image)

  fraction = math.floor(width/3)

  first = image[:, 0:fraction]
  second = image[:, fraction:2*fraction]
  third = image[:, 2*fraction:]

  return (first, second, third)

def get_barcodes(image):
  data = None
  decoded = decode_image(image)
  
  for barcode in decoded:
    data = barcode.data.decode("utf-8")

  return data

def correct_image_orientation(image):
  (height, width) = get_image_properties(image)
  
  if(width > height):
    (first, second, third) = split_image_in_thirds(image)

    first_histogram = get_grayscale_histogram(first)
    third_histogram = get_grayscale_histogram(third)

    first_black_level = first_histogram[0]
    third_black_level = third_histogram[0]

    if(first_black_level > third_black_level):
      return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
  
  else:
    (first, second) = split_image_in_half(image)

    first_histogram = get_grayscale_histogram(first)
    second_histogram = get_grayscale_histogram(second)

    first_black_level = first_histogram[1]
    second_black_level = second_histogram[1]

    if(second_black_level > first_black_level):
      return cv2.rotate(image, cv2.ROTATE_180)
    
    else:
      return image

def image_blue_filter(image):
  lower_range = np.array([110,50,50])
  upper_range = np.array([130,255,255])
  
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  return cv2.inRange(hsv, lower_range, upper_range)



def procces_image(path, output_path):
  image = read_image(path)
  image = correct_image_orientation(image)

  (first_half, second_half) = split_image_in_half(image)
  first_barcode = get_barcodes(first_half)
  second_barcode = get_barcodes(second_half)
  
  if(first_barcode == second_barcode):
    image = image_blue_filter(image)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    write_image(output_path, image)