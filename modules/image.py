import os
from os import listdir, path, remove

import cv2
import requests
from dotenv import load_dotenv
from easyocr import easyocr
from fastapi import HTTPException

from models.getData_model import GetDataModel
from modules.ftp_module.ftp import get_path_files, upload_file
from modules.querys_db.clientes.create_customer import create_customer
from modules.querys_db.imagen.create_image import create_image
from modules.querys_db.registro.create_register import create_register, delete_register
from modules.querys_db.registro.update_register import update_register

load_dotenv()

loyalty_url_prod = os.getenv("URL_LOYALTY_WS")


def get_user_id(path_str: str):
    ids = path_str.split("-")
    if ids != -1:
        customer_id = ids[1]
        id_registro = ids[0]
        return customer_id, id_registro
    return False


def filter_data(data: str):
    data_filter = data.find(":")
    if data_filter != -1:
        new_data = data[data_filter + 1 :]
        return new_data
    return data


def read_image(img_path: str):
    if img_path != None:
        reader = easyocr.Reader(lang_list=["es"], gpu=False, verbose=False)
        image = cv2.imread(img_path)
        result = reader.readtext(image, batch_size=3, width_ths=0.5, detail=0)
        result = list(filter(len, result))
        result = [data.lower() for data in result]
        return result


def create_data_object(data_ocr: list):
    position = 0
    firma = 0
    data_to_validate = {}
    document_number = ""
    for data in data_ocr[0:10]:
        position += 1
        if "ipcion" in data or "ipción" in data:
            data_to_validate["fecha_inscripcion"] = data_ocr[position]
        elif "dula" in data:
            for number in data_ocr[position]:
                if number.isdigit():
                    document_number += number
            data_to_validate["num_documento"] = document_number
    for data_firma in data_ocr[len(data_ocr) - 25 : len(data_ocr)]:
        if "firma:" in data_firma or "firma" in data_firma:
            firma = 1
        else:
            firma = 0
    return data_to_validate, firma


def validate_data_loyalty(data_to_validate: GetDataModel):
    data_to_send = {
        "sourceType": "POS",
        "docType": "CC",
        "docNumber": data_to_validate["num_documento"],
    }
    try:
        res = requests.post(url=loyalty_url_prod, json=data_to_send)
        res = res.json()
        response_code = res["response"]
        if response_code["responseCode"] == 0:
            customer_data = {}
            customer_data["id_tipo_doc"] = 1
            customer_data["num_documento"] = res["client"]["clientId"]["number"]
            customer_data["nombre_cliente"] = res["client"]["name"]["firstName"]
            customer_data["apellido_cliente"] = res["client"]["name"]["firstSurname"]
            customer_data["email_cliente"] = res["client"]["email"]
            for program in res["client"]["groups"]:
                if program["groupValue"]["groupName"] == "CLUB CRUZ VERDE":
                    fecha_inscripcion = program["creationSource"]["date"]
            return customer_data, fecha_inscripcion
        else:
            return False
    except HTTPException as httperror:
        print({"message": httperror})


def get_data():
    try:
        image_dir = "./temp"
        abs_image_dir = path.abspath(image_dir)
        data_dir = listdir(abs_image_dir)
        print(data_dir)
        print(len(data_dir))
        image_to_save = {}
        for image_file in data_dir:
            print("Cargando imagen...")
            print(image_file)
            id_user = get_user_id(image_file)
            last_image_path = f"{abs_image_dir}/{image_file}"
            ocr_data = read_image(last_image_path)
            id_registro = id_user[1]
            data_to_validate = create_data_object(ocr_data)
            if (
                "num_documento" in data_to_validate[0]
                and data_to_validate[0]["num_documento"] != ""
            ):
                data_from_loyalty = validate_data_loyalty(data_to_validate[0])
                if data_from_loyalty != False:
                    customer_data_loyalty = data_from_loyalty[0]
                    numero_doc_customer = create_customer(customer_data_loyalty)
                    update_register_data = {
                        "no_doc_cliente": numero_doc_customer,
                        "id_estado": 1,
                        "fecha_inscripcion": data_from_loyalty[1],
                        "firma": data_to_validate[1],
                    }
                    update_register(id_registro, update_register_data)
                    if customer_data_loyalty != False:
                        file_name = f"CC_{customer_data_loyalty['num_documento']}.jpg"
                        dir_destination = "coincide"
                        upload_file(
                            file_name=file_name,
                            destination_dir=dir_destination,
                            file_path=last_image_path,
                        )
                        path_ftp_file = get_path_files(dir_destination, file_name)
                        image_to_save = {
                            "id_usuario": id_user[0],
                            "id_registro": id_registro,
                            "nombre_archivo": file_name,
                            "path_archivo": path_ftp_file,
                        }
                        create_image(image_to_save)
                else:
                    update_register(id_registro, {"id_estado": 2})
                    dir_destination = "no_data"
                    path_ftp_file = get_path_files(dir_destination, image_file)
                    upload_file(
                        file_name=f"{image_file}",
                        file_path=last_image_path,
                        destination_dir=dir_destination,
                    )
                    image_to_save = {
                        "id_usuario": id_user[0],
                        "id_registro": id_registro,
                        "nombre_archivo": image_file,
                        "path_archivo": path_ftp_file,
                    }
                    create_image(image_to_save)
            else:
                update_register(id_registro, {"id_estado": 2})
                dir_destination = "no_data"
                path_ftp_file = get_path_files(dir_destination, image_file)
                upload_file(
                    file_name=f"{image_file}",
                    file_path=last_image_path,
                    destination_dir=dir_destination,
                )
                image_to_save = {
                    "id_usuario": id_user[0],
                    "id_registro": id_registro,
                    "nombre_archivo": image_file,
                    "path_archivo": path_ftp_file,
                }
                create_image(image_to_save)
            remove(last_image_path)
            print("La imagen se proceso correctamente")
    except Exception as e:
        print(e)
        delete_register(id_registro)
        remove(last_image_path)
        return {
            "message": "La imagen no pudo ser enviada. Inténtalo más tarde.",
            "status_code": 500,
        }
    return {"message": "La imagen se procesó correctamente", "status_code": 200}


def crear_registro():
    try:
        id_registro = create_register(id_estado=5)
        return id_registro
    except Exception as e:
        print(e)
