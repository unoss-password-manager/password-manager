import os
import shutil

def setupData():
    if (os.path.exists("./dat")):
        os.rename("./dat", "./dat_backup")
        os.makedirs("./dat")

def tearDown():
    if (os.path.exists("./dat_backup")):
        shutil.rmtree("./dat", ignore_errors=False, onerror=None)
        os.rename("./dat_backup", "./dat")
