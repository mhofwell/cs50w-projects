from django.http.response import HttpResponse
import requests
import shutil
import os.path
from os import path

# Path variables
MEDIA_ROOT = 'auctions/static/images'


# Util functions


def download_img(request, url, form):
    # set up all variables
    user_id = str(request.user.id)
    title = form.cleaned_data["title"]
    filename = url.split("/")[-1]
    # download the image from URL
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print("Image Successfully Downloaded:", filename)
    else:
        print("Image could not be retrieved.")
        return HttpResponse("We're sorry but the image could not be found!")
    # manage folder creation and moving the file to the right directory
    path = os.path.join(MEDIA_ROOT, user_id)
    print(path)
    # If user directory exists
    if os.path.isdir(path):
        listing_path = os.path.join(path, title)
        print(listing_path)
        # If project directory exists inside user directory
        if os.path.isdir(listing_path):
            shutil.move(filename, listing_path)
            print(f"{filename} successfuly moved to:", listing_path)
            return listing_path
        else:
            os.mkdir(listing_path)
            shutil.move(filename, listing_path)
            print(f"{filename} successfuly moved to:", listing_path)
            return listing_path
    # if user directory doesn't exist make the entire path to the image auctions/static/images/2/title/img.jpg
    else:
        usr_dir = MEDIA_ROOT+"/"+user_id
        print(usr_dir)
        os.mkdir(usr_dir)
        listing_dir = usr_dir+"/"+title
        print(listing_dir)
        os.mkdir(listing_dir)
        shutil.move(filename, listing_dir)
        print(f"{filename} successfuly moved to:", listing_dir)
        return listing_dir
