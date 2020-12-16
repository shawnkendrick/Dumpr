import re
import auth
import time
import random
import os, sys
import requests
import flickrapi

photo_details = []
url_pattern = '_o.jpg' 
photo_set_details = []

try: 
    flickr = flickrapi.FlickrAPI(auth.api_key, auth.api_secret, format='parsed-json')
    sets = flickr.photosets.getList(user_id = auth.user_id)
    photo_sets = sets['photosets']['photoset']
except Exception:
    print(Exception)  

# get all ids for photos in sets
def get_photo_set_details():
    for item in photo_sets:
        # set names 
        set_name = item['title']['_content']
        set_name = format_set_name(set_name).lower()
        # set ids
        set_id = item['id']
        # photos in set, pass set id
        try:
            photos = flickr.photosets.getPhotos(photoset_id = set_id) 
            # id for each photo
            for item in photos['photoset']['photo']:
                for key, value in item.items():
                    if key == 'id':
                        photo_id = value
                        print('Processing: ' + set_name)
                        photo_set_details.append([set_name, photo_id])
        except Exception:
            print(Exception)  

    # pass set details: set names, photo ids            
    get_photo_urls(photo_set_details)


# format set names
def format_set_name(set_name):
    for item in [',',':',' ', '|','-','.','_']:
        if item in set_name:
            set_name = set_name.replace(item, '_')
    return(set_name)     


# get image url by image id
def get_photo_urls(photo_set_details): 
    for detail in photo_set_details:
        try:           
            set_name = detail[0]
            photo_id = detail[1]
            # get photo sizes & urls 
            photo_sizes = flickr.photos.getSizes(photo_id = photo_id)
            # get image urls
            for item in photo_sizes['sizes']['size']:
                for key, value in item.items():
                    if key == 'source' and re.search(url_pattern, value):
                        photo_url = value
                        if set_name and photo_url:
                            print('Processing: ' + photo_url + ' in: ' + set_name)
                            photo_details.append([set_name, photo_url]) 
        except Exception:
            print(Exception)  

    create_photo_directories(photo_details)        


# create album directories
def create_photo_directories(photo_details):        
    for item in photo_details:
        dir_name =  item[0]
        if not os.path.isdir(dir_name):
            print('Creating directory: ' + dir_name)
            os.mkdir(dir_name)    
    save_photos(photo_details)  


# download and save photos 
def save_photos(photo_details):    
    for item in photo_details:
        dir_name = item[0]
        photo_url = item[1]
        photo_filename_number = random.randint(0, 10000) 
        photo_filename = dir_name + '_' + str(photo_filename_number) + '.jpg'
        save_path = './' + dir_name
        try:
            image_request = requests.get(photo_url, stream = True)
            time.sleep(3)
            full_save_path = os.path.join(save_path, photo_filename)   
            print('Downloading: ' + full_save_path)      
            open(full_save_path, 'wb').write(image_request.content)  
        except requests.ConnectionError as e:
            print(e)     
 

get_photo_set_details()