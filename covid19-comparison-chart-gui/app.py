import eel, sys, platform
from python.data import getAllCountries, getData

eel.init('web')

try:
    eel.start('main.html', mode='chrome', port=0, size=(1280, 720))
except EnvironmentError:
    if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
        eel.start('main.html', mode='edge', port=0, size=(1280, 720))
    else:
        raise
    
