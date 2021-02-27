import subprocess, os
import requests
import base64
import json

"""Config"""
rotation_time = 45  # seconds

accepted_extension = [".jpg", ".png"]
key = "53ca7503fc71be24856a9fd84c354cdd"
saved_url_path = "saved_url.json"
"""Config"""


def get_image(img_path):
    with open(img_path, "rb") as image_file:
        encoded_img = base64.b64encode(image_file.read())
    return encoded_img


def imgbb_api_call(img):

    payload = {"key": key, "image": img}

    try:
        return requests.post("https://api.imgbb.com/1/upload", data=payload)
    except:
        print("Can't reach API")


def upload_images_and_get_url():

    urls = []

    path = os.getcwd() + "/"
    for filename in os.listdir(path):
        print("Working on " + filename)
        flag = False
        for extension in accepted_extension:
            if filename.endswith(extension):
                flag = True
        if flag:
            img = get_image(path + filename)
            url = imgbb_api_call(img).json()["data"]["image"]["url"]
            urls.append(url)
    return urls


def get_already_done_urls():

    with open(saved_url_path) as json_file:
        urls = json.load(json_file)

    return urls


def save_already_done_urls(urls):

    with open(saved_url_path, "w") as outfile:
        json.dump(urls, outfile)


def generate_keyframes(urls):

    css_keyframes = "@keyframes background_rotation {\n"
    for i, url in enumerate(urls):
        percentage = round((100 / len(urls)) * i)
        css_keyframes += (
            "   " + str(percentage) + "%" + "{\n      --bg: url(" + url + ");\n   }\n\n"
        )

    percentage = 100
    css_keyframes += (
        "   " + str(percentage) + "%" + "{\n      --bg: url(" + urls[0] + ");\n   }\n"
    )
    css_keyframes += "}\n\n"

    return css_keyframes


def generate_CSS_code(urls):

    saved_urls = get_already_done_urls()
    for url in saved_urls:
        if url not in urls:
            urls.append(url)

    CSS_code = (
        "body {\n   height: 100%;\n\n   /* nb_background: Number of background you will have (see below)*/\n   /* rotation_time: Duration between each rotation*/\n   --nb_backgrounds: "
        + str(len(urls))
        + ";\n   --rotation_time:"
        + str(rotation_time)
        + "s;\n\n   animation: background_rotation calc(var(--nb_backgrounds) * var(--rotation_time)) linear 0s infinite;\n}\n\n"
        + generate_keyframes(urls)
        + "/* To hide the catbox video and let your background shine */\n#qpVideoHider.qpVideoOverlay {\n   background-color: rgb(0 0 0 / 0%);\n}\n\n/* To hide Countdown and let your background shine */\n#qpVideoOverflowContainer {\n   background: rgba(0, 0, 0, 0);\n}"
    )
    return CSS_code


def process():

    ##urls = upload_images_and_get_url()
    # save_already_done_urls(urls)
    urls = ["salut"]
    css_code = generate_CSS_code(urls)
    f = open("CSS_Code.txt", "w")
    f.write(css_code)
    f.close()


if __name__ == "__main__":

    process()
