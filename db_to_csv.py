import pandas as pd
import sqlite3
import os

conn = sqlite3.connect('labels.db')
im_names = pd.read_sql('SELECT id, imageName FROM images', conn) # take the whole 'labels' table from database
cat_names = pd.read_sql('SELECT id, categoryName FROM categories', conn)
assignments = pd.read_sql('SELECT category_id, image_id FROM labels', conn)

# extract filenames from pathnames
for index, row in im_names.iterrows(): 
    fname = os.path.basename(row['imageName'])
    im_names.at[index, 'imageName'] = fname
    print(fname)

names_join = pd.merge(assignments, im_names, left_on='image_id', right_on='id', how='left')
all_join = pd.merge(names_join, cat_names, left_on='category_id', right_on='id', how='left')


# get rid of unnecessary columns
all_join.drop('id_x', inplace=True, axis=1)
all_join.drop('id_y', inplace=True, axis=1)
all_join.drop('image_id', inplace=True, axis=1)
all_join.drop('category_id', inplace=True, axis=1)

# save labels
all_join.to_csv('labels.csv', index=False)
