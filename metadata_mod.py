import pandas as pd
import piexif

# filepath to the excel with all the photos and their info
photo_list = r'P:\Projects\2016\South Wing and Pavilion\South Pavilion\Digital Photos\South Pavilion Photo List 2.1.2019.xlsx'

# read the excel into a pandas dataframe
md_df = pd.read_excel(photo_list, cols=['DESCRIPTION', 'DIRECTION', 'INITIALS', 'SourceFile'])

for index, row in md_df.iterrows():

    print('reading in exif for %s...' % row['SourceFile'])
    exif = piexif.load(row['SourceFile'])

    ## exif tags
    # 270 --> ImageDescription
    # 315 --> Artist

    # set artist
    exif['0th'][315] = row['INITIALS'] + ", Thomas Jefferson's Monticello"

    # set description with direction
    exif['0th'][270] = row['DESCRIPTION']
    if row['DIRECTION'] != '':
        exif['0th'][270] += ', view %s' % row['DIRECTION']

    # convert exif to bytes to prep loading into file
    exif_bytes = piexif.dump(exif)

    # replace existing exif with modified copy
    print('  ...replacing exif!')
    piexif.insert(exif_bytes, row['SourceFile'])

