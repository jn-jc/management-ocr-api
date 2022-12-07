from easyocr import easyocr
import cv2
from os import path, listdir, remove

# remove(f'{abs_image_dir}/{last_image}')


def validate_image_dir():
    image_dir = "./temp"
    abs_image_dir = path.abspath(image_dir)
    data_dir = listdir(abs_image_dir)
    if len(data_dir) > 0:
        last_image_path = f"{abs_image_dir}/{data_dir[len(data_dir)-1]}"
        return last_image_path
    else:
        return False


def read_image():
    image_path = validate_image_dir()
    if image_path != False:
        print("Cargando imagen...")
        reader = easyocr.Reader(lang_list=["es"], gpu=False, verbose=False)
        image = cv2.imread(image_path)
        result = reader.readtext(image, batch_size=3, width_ths=0.5, detail=0)
        result = list(filter(len, result))
        result = [data.lower() for data in result]
        return result, image_path


def create_data_object():
    data = read_image()
    data_list = data[0]
    image_path = data[1]
    position = 0
    data_object = {}
    for data in data_list[0:25]:
        position += 1
        if "club cruz verde" in data or "dermo" in data:
            data_object["programa"] = data
        elif "ipcion" in data or "ipción" in data:
            data_object["fecha_inscripcion"] = data_list[position]
        elif "dula" in data:
            data_object["num_documento"] = data_list[position]
        elif "nombre:" in data:
            data_object["nombre"] = data
        elif "ape" in data:
            data_object["apellido"] = data
        elif "celular" in data:
            data_object["telefono"] = data
        elif "vendedor" in data:
            data_object["vendedor"] = data
    return data_object, image_path


def validate_data():
    data = create_data_object()
    #remove(data[1])
    print(data[0])
