# Special Character Macro

## What it does
Let you use macro for typing stuff in chat

Currently, the script let you press f2 to type ō and f4 to type ū, and ctrl+1 to type @husahusahusahusa (fuck his name)

## Usage
### How to download it
Download tampermonkey, and copy and paste the content of the .js file in a new tampermonkey script

### How to use it
#### Customize it
If you wish to change the keys and/or add other special characters, you just have to duplicate the code and change certain values:

```
if(event.keyCode=='113') {
    if(quiz.answerInput.inFocus){
        document.getElementById('qpAnswerInput').value += "ō";
    }
    else{
        document.getElementById('gcInput').value += "ō";
    }
}
```
If you want to change the key you have to press: you can go this site to get the right keycode for the key: https://keycode.info/, and then replace the "113" value with it.

If you want to change what it will write, just change the "ō" anywhere needed.

If you want to add multiple keys (for example CTRL+2), you just have to separate each key with "&&" in the if statement as such:
`if((event.keyCode=='17') && (event.keyCode=='50'))`
