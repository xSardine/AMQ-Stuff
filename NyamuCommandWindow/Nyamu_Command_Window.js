// ==UserScript==
// @name         AMQ Nyamu's Command Window
// @namespace    https://github.com/xSardine
// @version      1.0
// @author       Nyamu & xSardine
// @description  Let you type commands in a window instead of in chat
// @match        https://animemusicquiz.com/*
// @grant        none
// @require      https://raw.githubusercontent.com/TheJoseph98/AMQ-Scripts/master/common/amqScriptInfo.js
// @require      https://raw.githubusercontent.com/TheJoseph98/AMQ-Scripts/master/common/amqWindows.js
// @require      https://github.com/nyamu-amq/amq_scripts/raw/master/amqChatCommands.user.js
// ==/UserScript==

if (document.getElementById('startPage')) {
    return
}

// Change second value to change the code for the command
let commandMapping = {
    //host in lobby
    "/t": "/t",
    "/n": "/n",
    "/d": "/d",
    "/random": "/random",
    "/watched": "/watched",
    "/s": "/s",
    "/spec": "/spec",
    "/kick": "/kick",
    "/host": "/host",

    //host in game
    "/lb": "/lb",
    "/pause": "/pause",

    //anyone in lobby
    "/spec": "/spec",
    "/join": "/join",
    "/queue": "/queue",

    //anyone in game
    "/v": "/v",
    "/skip": "/skip",
    "/autothrow": "/autothrow",
}


let NyamuCommandWindow;
let flagCreated = false;
var target, settings, autothrow = '';

/* Command Window */
function createCommandWindow() {
    //if (!window.setupDocumentDone) return;
    NyamuCommandWindow = new AMQWindow({
        title: "Nyamu's command",
        position: {
            x: 0,
            y: 34
        },
        width: 400,
        height: 140,
        minWidth: 400,
        resizable: true,
        draggable: true
    });

    NyamuCommandWindow.addPanel({
        id: "NyamuCommandWindowPanel",
        width: 1.0,
        height: 1.0
    });

    NyamuCommandWindow.panels[0].panel
        .append($(`<input id="slCommand" type="text" placeholder="Command line">`)
            .on("keyup", function (event) {
                if (event.keyCode == 13) {
                    let commandQuery = $("#slCommand").val();
                    document.getElementById('slCommand').value = '';
                    for (var key in commandMapping) {
                        if (commandMapping.hasOwnProperty(key)) {
                            commandQuery = commandQuery.replace(key, commandMapping[key])
                        }
                    }
                    let payload = { sender: selfName, message: commandQuery }
                    console.log(payload)
                    processChatCommand(payload);
                }
            })
        )
}

function dockeyup(event) {
    if (event.altKey && event.keyCode == 80) { //alt+p
        if (!flagCreated) {
            createCommandWindow();
            flagCreated = true;
        }
        if (NyamuCommandWindow.isVisible()) {
            NyamuCommandWindow.close();
        }
        else {
            NyamuCommandWindow.open();
        }
    }
}
document.addEventListener('keyup', dockeyup, false);
/* Command Window */


/* CSS */
AMQ_addStyle(`
        #slCommand {
            width: 350px;
            color: black;
            margin: 15px 15px 0px 15px;
            height: 35px;
            border-radius: 4px;
            border: 0;
            text-overflow: ellipsis;
            padding: 5px;
            float: left;
        }
    `);

