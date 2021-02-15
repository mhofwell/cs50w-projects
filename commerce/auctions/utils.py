from commerce.settings import STATIC_URL
from django.http.response import HttpResponse
import requests
import shutil
import os.path
from os import path

# Util functions


def download_img(url):
    # set up all variables
    filename = url.split("/")[-1]
    # download the image from URL
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print("Image Successfully Downloaded:", filename)
        return filename
    else:
        print("Image could not be retrieved.")
        return HttpResponse("We're sorry but the image could not be found!")


def organize_img(request, filename, form):
    user_id = str(request.user.id)
    title = form.cleaned_data["title"]

    user_root = os.path.join('auctions/'+STATIC_URL, 'images/'+user_id)
    listing_root = os.path.join(user_root, title)
    image_path = os.path.join(listing_root, filename)

    if os.path.isdir(user_root) and os.path.isdir(listing_root):
        print("Directories already exist!")
    elif not os.path.isdir(user_root):
        os.mkdir(user_root)
        os.mkdir(listing_root)
    else:
        os.mkdir(listing_root)

    shutil.move(filename, listing_root)
    print(f"{filename} successfuly moved to:", image_path)
    return "images/"+user_id+"/"+title+"/"+filename
