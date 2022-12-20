import ftplib


FTP_SERVER = '10.182.34.76'
FTP_USER = 'testCO'
FTP_PASS = 'testCO_2020'


def upload_file (destination_dir, file_name, file_path):
  ftp = ftplib.FTP(FTP_SERVER, FTP_USER, FTP_PASS) 

  ftp.cwd(f'./{destination_dir}')

  with open(file_path, 'rb') as archivo:
    ftp.storbinary(f'STOR {file_name}', archivo)
    
  ftp.quit()
  
def get_path_files (dir: str, file_name: str):
  ftp = ftplib.FTP(FTP_SERVER, FTP_USER, FTP_PASS) 
  ftp.cwd(f'./{dir}')
  file_path = f'{ftp.pwd()}/{file_name}'
  ftp.quit()
  return file_path

