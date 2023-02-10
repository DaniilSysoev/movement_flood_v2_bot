import datetime
from script_for_all_b import start_script


while True:
    if datetime.datetime.now().hour == 0 and datetime.datetime.now().minute == 0:
        start_script()
        break