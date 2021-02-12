import requests
import shutil


def download_img(url):
    filename = url.split("/")[-1]
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print("Image Successfully Downloaded: ", filename)
        shutil.move(filename, 'auctions/static/images')
        print("Image Successfully Moved: ", filename)
        return filename
    else:
        print("Image could not be retrieved.")
