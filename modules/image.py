from easyocr import easyocr
import cv2
from os import path, listdir, remove

data_object = {
    'programa': '',
    'fecha_inscripcion': '',
    'cedula': '',
    'nombre': '',
    'apellido': '',
    'celular': '',
    'vendedor': ''
  }

def validate_image():
    image_dir = "./temp"
    abs_image_dir = path.abspath(image_dir)
    data_dir = listdir(abs_image_dir)
    if len(data_dir) > 0:
        last_image_path = f"{abs_image_dir}/{data_dir[len(data_dir)-1]}"
        return last_image_path
        # remove(f'{abs_image_dir}/{last_image}')
    else:
        return False


def read_image():
    image_path = validate_image()
    if image_path != False:
        print("Cargando imagen...")
        reader = easyocr.Reader(lang_list=["es"], gpu=False, verbose=False)
        image = cv2.imread(image_path)
        result = reader.readtext(image, batch_size=5, width_ths=0.5 ,detail=0)
        result = list(filter(len, result))
        result = [data.lower()for data in result]
        return result
      
def create_data_object():
  data_list = read_image()
  print(data_list)
  position = 0
  for data in data_list:
    position += 1
    if 'club cruz verde' in data or 'dermo' in data:
      data_object['programa'] = data
    elif 'ipcion' in data or 'ipción' in data:
      data_object['fecha_inscripcion'] = data
    elif 'dula' in data:
      data_object['cedula'] = data_list[position]
    elif 'nombre:' in data:
      data_object['nombre'] = data
    elif 'ape' in data:
      data_object['apellido'] = data
    elif 'celular' in data:
      data_object['celular'] = data
    elif 'vendedor' in data:
      data_object['vendedor'] = data
  print(data_object) 
  # print(data_list[0:30])
