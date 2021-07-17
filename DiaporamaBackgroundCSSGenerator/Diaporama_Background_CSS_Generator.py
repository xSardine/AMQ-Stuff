import subprocess, os
import requests
import base64
import json

"""Config"""
rotation_time = 45  # seconds

accepted_extension = [".jpg", ".png", "jpeg"]
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
        return {"Error": "Can't reach API"}


def is_acceptable_extension(filename):
    flag = False
    for extension in accepted_extension:
        if filename.endswith(extension):
            flag = True
    return flag


def is_image_already_uploaded(urls, img_name):

    for img_file in urls:
        if img_name == img_file["name"]:
            return True
    return False


def write_error_file(errors):

    msg = ""
    for error in errors:
        msg += error["name"] + ": " + error["error"] + "\n"

    f = open("not_uploaded.txt", "w")
    f.write(msg)
    f.close()


def upload_images_and_get_url(urls):

    errors = []

    path = os.getcwd() + "/"
    for filename in os.listdir(path):
        print("Working on " + filename + "...")
        if is_acceptable_extension(filename):
            if not is_image_already_uploaded(urls, filename):
                img = get_image(path + filename)
                response = imgbb_api_call(img).json()
                if "data" in response:
                    url = response["data"]["image"]["url"]
                    urls.append({"name": filename, "url": url})
                    save_already_done_urls(urls)
                    print("Uploaded!\n")
                else:
                    print("Problem with the response:", response, "\n")
                    errors.append(
                        {
                            "name": filename,
                            "error": "Problem with the response:"
                            + str(response)
                            + "\n",
                        }
                    )
            else:
                print(
                    "This file has already been uploaded (change its name if it hasn't)\n"
                )
                errors.append(
                    {
                        "name": filename,
                        "error": "This file has already been uploaded (change its name if it hasn't)\n",
                    }
                )
        else:
            if (
                not filename.endswith(".py")
                and not filename.endswith(".txt")
                and not filename.endswith(".exe")
                and not filename.endswith(".json")
            ):
                print("Not a valid format: Ignored\n")
                errors.append(
                    {"name": filename, "error": "Not a valid image: Ignored\n"}
                )
            else:
                print()

    if len(errors) > 0:
        write_error_file(errors)

    return urls


def get_already_done_urls():

    if os.path.isfile(saved_url_path):
        with open(saved_url_path) as json_file:
            urls = json.load(json_file)
        return urls
    else:
        print(
            "No save found, if you had one, make sur it's called saved_url.json and it is in the right directory.\n"
        )
        return []


def save_already_done_urls(urls):

    with open(saved_url_path, "w") as outfile:
        json.dump(urls, outfile)


def generate_keyframes(urls):

    css_keyframes = "@keyframes background_rotation {\n"
    for i, img_file in enumerate(urls):
        percentage = (100 / len(urls)) * i
        css_keyframes += (
            "   "
            + str(percentage)
            + "%"
            + "{\n      --bg: url("
            + img_file["url"]
            + ");\n   }\n\n"
        )

    percentage = 100
    css_keyframes += (
        "   "
        + str(percentage)
        + "%"
        + "{\n      --bg: url("
        + urls[0]["url"]
        + ");\n   }\n"
    )
    css_keyframes += "}\n\n"

    return css_keyframes


def generate_CSS_code(urls):

    CSS_code = ""
    print("Generating CSS code for ", len(urls), "images...")

    if len(urls) > 0:

        CSS_code = (
            "body {\n   height: 100%;\n\n   /* nb_background: Number of backgrounds you have*/\n   /* rotation_time: Duration between each rotation*/\n   --nb_backgrounds: "
            + str(len(urls))
            + ";\n   --rotation_time:"
            + str(rotation_time)
            + "s;\n\n   animation: background_rotation calc(var(--nb_backgrounds) * var(--rotation_time)) linear 0s infinite;\n}\n\n"
            + generate_keyframes(urls)
            + "/* If any of these don't work, make sure the rest of Elodie's script isn't overwriting any of these */\n/* To hide the video during loading phase */\n#qpVideoOverflowContainer {\n   box-shadow: none;\n   background: rgba(0, 0, 0, 0);\n}\n\n/* To hide the black screen during guessing phase */\n#qpVideoHider.qpVideoOverlay {\n   background-color: rgb(0 0 0 / 0%);\n}\n\n/* To hide the countdown during guessing phase */\n.qpVideoOverlay > div {\n    top: 115%;\n}"
        )

    return CSS_code


def process():

    urls = get_already_done_urls()
    urls = upload_images_and_get_url(urls)
    if len(urls) > 0:
        save_already_done_urls(urls)
        css_code = generate_CSS_code(urls)
        f = open("CSS_Code.css", "w")
        f.write(css_code)
        f.close()
    else:
        print("No valid image files detected")


if __name__ == "__main__":

    process()
