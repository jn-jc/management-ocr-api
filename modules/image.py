from easyocr import easyocr
import cv2
from os import path, listdir, remove



def validate_image():
  image_dir = './temp'
  abs_image_dir = path.abspath(image_dir)
  data_dir = listdir(abs_image_dir)
  if len(data_dir) > 0:  
    last_image_path = f'{abs_image_dir}/{data_dir[len(data_dir)-1]}' 
    return last_image_path
    #remove(f'{abs_image_dir}/{last_image}')
  else:
    return False
    
def read_image():
  reader = easyocr.Reader(lang_list=['es'], gpu=False)
  image_path = validate_image()
  if image_path != False:
    image = cv2.imread(image_path)
    result = reader.readtext(image)
    print (result)
    for res in result[0:15]:
      print(f'data: {res[1]}')