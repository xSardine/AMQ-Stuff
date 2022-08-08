// ==UserScript==
// @name         AMQ Player Picker
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Player Picker: select randomly one or multiple players in the AMQ room and @ them. Type "/pickplayer x" to pick x players from the lobby (if no number specified, default to 1)
// @author       xSardine
// @match        https://animemusicquiz.com/*
// @grant        none
// @copyright    MIT license
// @downloadURL  https://github.com/xSardine/AMQ-Stuff/raw/main/pickRandomPlayer/pickRandomPlayer.user.js
// @updateURL    https://github.com/xSardine/AMQ-Stuff/raw/main/pickRandomPlayer/pickRandomPlayer.user.js
// @require      https://raw.githubusercontent.com/TheJoseph98/AMQ-Scripts/master/common/amqScriptInfo.js
// ==/UserScript==

// don't load on login page
if (document.getElementById('startPage')) return;

// Wait until the LOADING... screen is hidden and load script
let loadInterval = setInterval(() => {
    if (document.getElementById("loadingScreen").classList.contains("hidden")) {
        setup();
        clearInterval(loadInterval);
    }
}, 500);


//Initialize listeners and 'Installed Userscripts' menu
function setup() {
    new Listener("Game Chat Message", (payload) => {
        processChatMessage(payload);
    }).bindListener();
    new Listener("game chat update", (payload) => {
        payload.messages.forEach(message => {
            processChatMessage(message);
        });
    }).bindListener();
    AMQ_addScriptData({
        name: "AMQ Player Picker",
        author: "xSardine",
        description: `<p>select randomly one or multiple players in your AMQ lobby and @ them</p>
			<p>Type "/pickplayer x" to pick x players from the lobby (if no number specified, default to 1)</p>
            <p><a href="https://github.com/xSardine/AMQ-Stuff/raw/main/1SecondAudio/1Second_Audio.user.js">Click this link</a> to update it.</p>`
    });
}

function processChatMessage(payload) {
    let chatMessage = payload.message;
    if (payload.sender === selfName && chatMessage.startsWith("/pickplayer")) {
        if (lobby.inLobby) {

            let nbToPick = chatMessage.match(/\d/g);
            if (nbToPick) nbToPick = nbToPick.join("")
            else nbToPick = 1

            if (nbToPick == 1) sendChatMessage("Picking a random player...");
            else sendChatMessage(`Picking ${nbToPick} random players...`);

            let players = [];
            for (let playerId in lobby.players) {
                players.push(lobby.players[playerId]._name);
            }

            if (players.length < nbToPick) {
                sendChatMessage("There is not enough players in this lobby to pick that amount.");
                return
            }

            while (nbToPick > 0) {
                let pickedId = getRandomInt(players.length);
                sendChatMessage("@" + players[pickedId]);
                players.splice(pickedId, 1)
                nbToPick -= 1
            }

            players = [];
        }
        else {
            gameChat.systemMessage("Must be in pre-game lobby");
        }
    }
};

function sendChatMessage(message) {
    gameChat.$chatInputField.val(message);
    gameChat.sendMessage();
}

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}