# AMQ-Stuff
AMQ stuff I make because i'm bored

# Rotation background CSS generator

## What it does
Get an URL link automatically for all the files in the directory and generate CSS code necessary to add to Elodie's script

## Usage
### Requirement
You need python to make it work, it can be downloaded here: https://www.python.org/downloads/

### How to use it
#### First time
- Create a directory with main.py and every image files you want as background in it
- double click main.py, it will:
	- Upload every images to ImgBB: https://imgbb.com/
	- Save the URLs in a file named "saved_url.json"
	- Generate CSS code in a file named "CSS_code.txt"
- Remove the images you just uploaded from the directory, copy the content of "CSS_code.txt" and replace the "body" part of Elodie's script with it (Elodie script: https://userstyles.org/styles/179263/elodie-s-amq-script-v7-1)
- Launch AMQ

#### Adding new images:
As long as you kept the file "saved_url.json" and place it in the same directory as main.py, you will be able to just add new images to the background pool without having to re-uplaod what you already uploaded.
To add new images, just repeat the previous process (don't forget to remove what you already uploaded, so that you don't upload them twice)

#### Customization:
The countdown and catbox video are hidden by default, if you want either of them, you can remove the few last lines of the code generated. (It's commented, should be easy to find)
You can change the duration between each background change by modifying the value of "rotation_time" in the generated code
