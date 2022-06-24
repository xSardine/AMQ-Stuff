# Nyamu Command Windows

## What it does

Let you type nyamu's chat command in a personal windows instead of chat

Currently, the script let you press alt+p to open the command windows

Nyamu's script if you would rather use chat: <https://github.com/nyamu-amq/amq_scripts/blob/master/amqChatCommands.user.js>

## Usage

### How to download it

Download [tampermonkey](https://www.tampermonkey.net/), and add the [userscript](https://github.com/xSardine/AMQ-Stuff/raw/main/NyamuCommandWindow/Nyamu_Command_Window.user.js) to it.

### How to use it

#### Commands

it let you use Nyamu's command which are:

- commands for host in lobby
    - - /t [oei] : change songtype. ex) /t oi => openings inserts. /t ei => endings inserts. /t e => endings only.
    - - /n (number) : change number of songs
    - - /d (number1)-(number2) : change difficulty. ex) /d 0-40 => change difficulty to 0-40
    - - /random : change song selection to random
    - - /watched : change song selection to watched only
    - - /s (number) : change speed. amq allow one of 1, 1.5, 2, 4 only
    - - /spec (someone) : send someone to spec
    - - /kick (someone) : kick someone
    - - /host (someone) : give someone host
- commands for host in game
    - - /lb : start a vote for returning to lobby
    - - /pause : pause or unpause game
- commands for everyone in lobby
    - - /spec : change to spectator
    - - /join : change to player
    - - /queue : toggle queue when you are in lobby while game is progressing
- commands for everyone in game
    - - /v (number) : change volume 0-100
    - - /skip : skip current song
    - - /autothrow (answer) : start throwing with answer automatically. you can stop it by /autothrow without answer

#### Customize it

If you want to change the key you have to press to open the command window, you just have to change the values of `if(event.altKey && event.keyCode==80)` with what you want using this website: <https://keycode.info/>

You can also customize every command, if you want to type /at instead of /autothrow for example, you just have to change the second value in the `commandMapping` dictionary
