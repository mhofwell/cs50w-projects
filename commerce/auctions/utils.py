import requests
import shutil

IMG_ROOT = 'auctions/static/images'


def download_img(url):
    filename = url.split("/")[-1]
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print("Image Successfully Downloaded:", filename)
        shutil.move(filename, IMG_ROOT)
        print("Image Successfully Moved:", filename)
        return filename
    else:
        print("Image could not be retrieved.")
