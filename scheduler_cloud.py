import subprocess
import time

while True:
    # Launch the data_process.py script
    #res_cat = subprocess.Popen(['python3', '/home/io3/Desktop/codice_bk_2023_06_18/ms_resource_catalog/main_ms_resource_catalog.py'])
    cloud = subprocess.Popen(['python3', '/home/io3/Desktop/codice_bk_2023_06_18/ms_cloud/main_ms_cloud.py'])
    #data_process = subprocess.Popen(['python3', '/home/io3/Desktop/codice_bk_2023_06_18/ms_dataprocess/main_ms_dataprocess.py'])

    # Wait for an hour before running the script again
    time.sleep(1200)  # 3600 seconds = 1 hour
    
    #res_cat.terminate()
    cloud.terminate()
    #cloud.terminate()
    
