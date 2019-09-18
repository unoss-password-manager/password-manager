import os
import shutil

def setupData():
    if (os.path.exists("./dat")):
        os.rename("./dat", "./dat_backup")
        os.makedirs("./dat")

def tearDown():
    shutil.rmtree("./dat", ignore_errors=False, onerror=None)
    if (os.path.exists("./dat_backup")):        
        os.rename("./dat_backup", "./dat")
