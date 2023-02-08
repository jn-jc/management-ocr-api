
import paramiko


FTP_SERVER = '10.182.34.126'
FTP_USER = 'userDig'
FTP_PASS = 'M3dicart3'
FTP_PORT = 22


def upload_file (destination_dir, file_name, file_path):
  
  transport = paramiko.Transport((FTP_SERVER, FTP_PORT))
  transport.connect(username=FTP_USER, password=FTP_PASS)
  
  sftp = transport.open_sftp_client()
  sftp.put(localpath=file_path,remotepath=f'/ocr_app/{destination_dir}/{file_name}')
  sftp.close()
  transport.close()


def get_path_files (path_dir: str, file_name: str):
  
  return f'/ocr_app/{path_dir}/{file_name}'
  

