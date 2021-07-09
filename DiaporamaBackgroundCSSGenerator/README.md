# Diaporama Background CSS Generator

# **What it does**
Help you have multiple backgrounds as a diaporama for AMQ:

Get an URL link automatically for all the files in the directory and generate CSS code necessary to add to Elodie's script

# **Usage**
## **What to download**

Stylus for Elodie's script. (don't use stylish 🔫)

You need to have a python set with an environment variable in the PATH
To check, you can open your CMD and type python, and if you don't get any errors, you're good to go.

Install the dependencies:
```bash
python -m pip install requests
```

## **How to use it**
### **First time**
- Create a directory with Diaporama_Background_CSS_Generator.py and every image files you want as background in it
- double click Diaporama_Background_CSS_Generator, it will:
	- Upload every images to ImgBB: https://imgbb.com/ | This part may take some time if you have a lot of files / a bad connection, don't worry, it should eventually finish
	- Save the URLs in a file named "saved_url.json"
	- Generate CSS code in a file named "CSS_code.css"
- Remove the images you just uploaded from the directory, copy the content of "CSS_code.css" and add it to Elodie's script (https://userstyles.org/styles/179263/elodie-s-amq-script-v8-4-2), just put it under the "root" part for example :shrug: If you really don't know, you can check the example.css, which is my version of Elodie's code.
- Launch AMQ

### **Adding new images**
As long as you kept the file "saved_url.json" and place it in the same directory as Diaporama_Background_CSS_Generator.py, you will be able to just add new images to the background pool without having to re-upload what you already uploaded.

To add new images, just repeat the previous process (don't forget to remove what you already uploaded, so that you don't upload them twice)

### **Customization**
The countdown and catbox video are hidden by default, if you want either of them, you can remove the few last lines of the code generated. (It's commented, should be easy to find)

You can change the duration between each background change by modifying the value of "rotation_time" in the generated code