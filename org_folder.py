'''
Steps:

1. Extract dataset to a folder.
2. Move this script into that folder and run it (Should be at the same level as 'Phase02-DataDelivery').

'''


import os
import shutil
import re

try:
    os.mkdir('data')
except Exception:
    print('DIR exists')


masks = os.listdir('Phase02-DataDelivery/masks')
metadata = os.listdir('Phase02-DataDelivery/metadata')
dates = [os.path.splitext(data)[0] for data in metadata]

for mask in masks:
    mask = os.path.splitext(mask)[0]
    try:
        os.mkdir(f'data/{mask}')
    except Exception:
        pass
    search = '-'.join(re.findall('\d+', mask))
    photos = os.listdir('Phase02-DataDelivery/sugarcanetiles')
    for date in dates:
        os.mkdir(f'data/{mask}/{date}')
        shutil.copyfile(
            f'Phase02-DataDelivery/metadata/{date}.json', f'data/{mask}/{date}/metadata.json')
        for photo in photos:
            if search in photo and date in photo:
                Band = photo.replace('-', ' ').split(' ')[2]
                ext = os.path.splitext(photo)[1]
                shutil.copy2(
                    f'Phase02-DataDelivery/sugarcanetiles/{photo}', f'data/{mask}/{date}/{Band}{ext}')
