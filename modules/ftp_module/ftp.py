
import paramiko


FTP_SERVER = '172.18.50.27'
FTP_USER = 'geoproa'
FTP_PASS = 'G22pr0.22'
FTP_PORT = 22


def upload_file (destination_dir, file_name, file_path):
  
  transport = paramiko.Transport((FTP_SERVER, FTP_PORT))
  transport.connect(username=FTP_USER, password=FTP_PASS)
  
  sftp = transport.open_sftp_client()
  sftp.put(localpath=file_path,remotepath=f'./ocr_images/{destination_dir}/{file_name}')
  sftp.close()
  transport.close()


def get_path_files (path_dir: str, file_name: str):
  
  return f'./ocr_images/{path_dir}/{file_name}'
  

