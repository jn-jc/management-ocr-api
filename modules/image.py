from easyocr import easyocr
from fastapi import HTTPException
import cv2
import requests
from os import path, listdir, remove
from models.getData_model import GetDataModel
from models.cliente_model import ClienteModel
from models.registro_model import RegistroModel
from models.image_model import ImageModel
import os
from dotenv import load_dotenv
from modules.querys_db.registro.create_register import create_register
from modules.querys_db.registro.update_register import update_register
from modules.ftp_module.ftp import upload_file, get_path_files
from modules.querys_db.imagen.create_image import create_image
from modules.querys_db.clientes.create_customer import create_customer
from modules.querys_db.plan_clientes.create_plan_clientes import create_plan_cliente

load_dotenv()

loyalty_url_prod = os.getenv("URL_LOYALTY_WS")


def get_user_id(path_str: str):
    id_position = path_str.find("-")
    if id_position != -1:
        customer_id = path_str[:id_position]
        return customer_id
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
    data_to_validate: GetDataModel = {}
    document_number = ""
    for data in data_ocr[0:10]:
        position += 1
        if "club cruz verde" in data:
            data_to_validate["programa"] = "CCV"
        elif "dermo" in data:
            data_to_validate["programa"] = "CDC"
        elif "ipcion" in data or "ipción" in data:
            data_to_validate["fecha_inscripcion"] = data_ocr[position]
        elif "dula" in data:
            for number in data_ocr[position]:
                if number.isdigit():
                    document_number += number
            data_to_validate["num_documento"] = document_number
    return data_to_validate


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
            customer_data: ClienteModel = {}
            customer_program = {}
            customer_data["id_tipo_doc"] = 1
            customer_data["num_documento"] = res["client"]["clientId"]["number"]
            customer_data["nombre_cliente"] = res["client"]["name"]["firstName"]
            customer_data["apellido_cliente"] = res["client"]["name"]["firstSurname"]
            customer_data["email_cliente"] = res["client"]["email"]
            if data_to_validate["programa"] == "CCV":
                for program in res["client"]["groups"]:
                    if program["groupValue"]["groupName"] == "CLUB CRUZ VERDE":
                        customer_program["id_plan"] = 2
                        customer_program["fecha_inscripcion"] = program[
                            "creationSource"
                        ]["date"]
            elif data_to_validate["programa"] == "CDC":
                for program in res["client"]["groups"]:
                    if program["groupValue"]["groupName"] == "CLUB DERMO":
                        customer_program["id_plan"] = 1
                        customer_program["fecha_inscripcion"] = program[
                            "creationSource"
                        ]["date"]
            return customer_data, customer_program
        else:
            return False
    except HTTPException as httperror:
        print({"message": httperror})


def get_data():
    image_dir = "./temp"
    abs_image_dir = path.abspath(image_dir)
    data_dir = listdir(abs_image_dir)
    image_to_save: ImageModel = {}
    while len(data_dir) > 0:
        image_to_pop = data_dir.pop()
        id_user = get_user_id(image_to_pop)
        last_image_path = f"{abs_image_dir}/{image_to_pop}"
        ocr_data = read_image(last_image_path)
        id_registro = create_register()
        data_to_validate = create_data_object(ocr_data)
        if (
            "num_documento" in data_to_validate
            and data_to_validate["num_documento"] != "" 
            "programa" in data_to_validate
            and data_to_validate["programa"] != ""
        ):
            data_from_loyalty = validate_data_loyalty(data_to_validate)
            customer_data_loyalty = data_from_loyalty[0]
            program_data_loyalty = data_from_loyalty[1]
            numero_doc_customer = create_customer(customer_data_loyalty)
            program_data_loyalty["id_registro"] = id_registro
            create_plan_cliente(program_data_loyalty)
            update_register_data = {
                "no_doc_cliente": numero_doc_customer,
                "id_estado": 1,
            }
            update_register(id_registro, update_register_data)
            if customer_data_loyalty != False:
                file_name = f"CC_{customer_data_loyalty['num_documento']}-{data_to_validate['programa']}"
                dir_destination = "coincide"
                upload_file(
                    file_name=file_name,
                    destination_dir=dir_destination,
                    file_path=last_image_path,
                )
                path_ftp_file = get_path_files(dir_destination, file_name)
                image_to_save = {
                    "id_usuario": id_user,
                    "id_registro": id_registro,
                    "nombre_archivo": file_name,
                    "path_archivo": path_ftp_file,
                }
                create_image(image_to_save)
        else:
            dir_destination = "no_data"
            path_ftp_file = get_path_files(dir_destination, image_to_pop)
            upload_file(
                file_name=image_to_pop,
                file_path=last_image_path,
                destination_dir=dir_destination,
            )
            image_to_save = {
                "id_usuario": id_user,
                "id_registro": id_registro,
                "nombre_archivo": image_to_pop,
                "path_archivo": path_ftp_file,
            }
            create_image(image_to_save)
        remove(last_image_path)
