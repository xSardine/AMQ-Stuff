# Diaporama Background CSS Generator

# **What it does**

Help you have multiple backgrounds as a diaporama for AMQ:

The script will upload automatically to an image host all the image in its directory, and generate the code to add to Elodie's userscript.

# **Usage**

## **What to download**

Stylus for Elodie's script. (don't use stylish 🔫)

You need to download [python](https://www.python.org/downloads/). During the installation phase, don't forget to select the option that let you have python as a PATH system variable.

Install the script's depencencies by opening your CMD (windows search → cmd → open the first thing that appears) and typing:

```bash
python -m pip install requests
```

## **How to use it**

### **> First time**

- Create a directory with `Diaporama_Background_CSS_Generator.py` and every image files you want as background in it
- Open powershell in the created directory: `Shift + Right-Click` on the folder where your files are located, then click `Open PowerShell window here`

- You can then start the script by typing:

```py
python Diaporama_Background_CSS_Generator.py
```

- The script will automatically:
  - Upload every images to [ImgBB](https://imgbb.com/) | This part may take some time if you have a lot of files / a bad connection, don't worry, it should eventually finish
  - Save the URLs in a file named `saved_url.json`, try to not loose it
  - Generate CSS code in a file named `CSS_code.css`
- Once the script is done, copy the content of `CSS_code.css` and add it to [Elodie's script](https://userstyles.org/styles/179263/elodie-s-amq-script-v8-4-2), just put it under the "root" part for example :shrug: If you really don't know, you can check the `example_elodie_script.css`, which is my version of Elodie's code.
- A file `not_uploaded.txt` might appears if any of the file inside the directory are not successfully uploaded. If it does appear, you can check which one have failed and why.

### **> Adding new images**

As long as you kept the file `saved_url.json` and place it in the same directory as `Diaporama_Background_CSS_Generator.py`, you will be able to just add new images to the background pool without having to re-upload what you already uploaded.

To add new images, just repeat the previous process.

### **> I want to leave in the middle of the process**

If you would like to stop the process during the uploading phase, you should be able to do so without loosing your progress by just closing the powershell window. Just make sure to keep `saved_url.json` in hand so that you can start back where you ended.

### **> Customization**

The countdown and catbox video are hidden by default, if you want either of them, you can remove/modify the last few lines of the generated CSS code (It's commented, should be easy to find).

You can change the duration between each background swap by modifying the value of `rotation_time` in the generated CSS code.
