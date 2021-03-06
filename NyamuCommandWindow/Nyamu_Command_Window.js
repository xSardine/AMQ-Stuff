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
// ==/UserScript==

if (document.getElementById('startPage')) {
    return
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
                    let payload = { sender: selfName, message: commandQuery }
                    console.log(payload)
                    applyNyamuCommand(payload);
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


/* Nyamu userscript */
function applyNyamuCommand(payload) {
    if (payload.sender !== selfName) return;
    if (payload.message.startsWith("/s ")) {
        if (!lobby.inLobby) return;
        if (!lobby.isHost) return;
        var settings = hostModal.getSettings();
        settings.playbackSpeed.randomOn = false;
        settings.playbackSpeed.standardValue = payload.message.substr(3) * 1;
        changeGameSettings(settings);
    }
    if (payload.message.startsWith("/t ")) {
        if (!lobby.inLobby) return;
        if (!lobby.isHost) return;
        var types = payload.message.substr(3).toLowerCase();
        var op = types.includes('o');
        var ed = types.includes('e');
        var ins = types.includes('i');
        if (!op && !ed && !ins) return;
        settings = hostModal.getSettings();
        settings.songType.standardValue.openings = op;
        settings.songType.standardValue.endings = ed;
        settings.songType.standardValue.inserts = ins;
        settings.songType.advancedValue.openings = 0;
        settings.songType.advancedValue.endings = 0;
        settings.songType.advancedValue.inserts = 0;
        settings.songType.advancedValue.random = settings.numberOfSongs;
        changeGameSettings(settings);
    }
    if (payload.message.startsWith("/n ")) {
        if (!lobby.inLobby) return;
        if (!lobby.isHost) return;
        var numberOfSongs = payload.message.substr(3) * 1;
        if (numberOfSongs < 5) return;
        settings = hostModal.getSettings();
        settings.numberOfSongs = numberOfSongs;
        changeGameSettings(settings);
    }
    if (payload.message.startsWith("/d ")) {
        if (!lobby.inLobby) return;
        if (!lobby.isHost) return;
        var difs = payload.message.substr(3).split('-');
        if (difs.length < 2) return;
        difs[0] = difs[0] * 1;
        difs[1] = difs[1] * 1;
        settings = hostModal.getSettings();
        settings.songDifficulity.advancedOn = true;
        if (difs[0] < difs[1])
            settings.songDifficulity.advancedValue = [difs[0], difs[1]];
        else
            settings.songDifficulity.advancedValue = [difs[1], difs[0]];
        changeGameSettings(settings);
    }
    if (payload.message.startsWith("/random")) {
        if (!lobby.inLobby) return;
        if (!lobby.isHost) return;
        settings = hostModal.getSettings();
        settings.songSelection.standardValue = 1;
        settings.songSelection.advancedValue['watched'] = 0;
        settings.songSelection.advancedValue['unwatched'] = 0;
        settings.songSelection.advancedValue['random'] = settings.numberOfSongs;
        changeGameSettings(settings);
    }
    if (payload.message.startsWith("/watched")) {
        if (!lobby.inLobby) return;
        if (!lobby.isHost) return;
        settings = hostModal.getSettings();
        settings.songSelection.standardValue = 3;
        settings.songSelection.advancedValue['watched'] = settings.numberOfSongs;
        settings.songSelection.advancedValue['unwatched'] = 0;
        settings.songSelection.advancedValue['random'] = 0;
        changeGameSettings(settings);
    }
    else if (payload.message.startsWith("/v ")) {
        var volumetemp = payload.message.substr(3) * .01;
        volumetemp = Math.min(Math.max(volumetemp, 0), 100);
        volumeController.volume = volumetemp;
        volumeController.adjustVolume();
        volumeController.setMuted(false);
    }
    else if (payload.message.startsWith("/spec")) {
        if (!lobby.inLobby) return;
        if (payload.message.length > 6) {
            if (!lobby.isHost) return;
            target = payload.message.substr(6);
            if (!checkLobby(target)) return;
            lobby.changeToSpectator(target);
        }
        else {
            lobby.changeToSpectator(selfName);
        }
    }
    else if (payload.message.startsWith("/join")) {
        if (!lobby.inLobby) return;
        socket.sendCommand({
            type: "lobby",
            command: "change to player",
        });
    }
    else if (payload.message.startsWith("/queue")) {
        if (hostModal.gameMode === 'Ranked') return;
        if (!quiz.inQuiz) return;
        if (!quiz.isSpectator) return;
        gameChat.joinLeaveQueue();
    }
    else if (payload.message.startsWith("/kick ")) {
        if (!lobby.isHost) return;
        if (payload.message.length > 6) {
            target = payload.message.substr(6);
            if (!checkLobby(target) && !checkSpec(target)) return;
            socket.sendCommand({
                type: "lobby",
                command: "kick player",
                data: { playerName: target },
            });
        }
    }
    else if (payload.message.startsWith("/host ")) {
        if (!lobby.isHost) return;
        if (payload.message.length > 6) {
            target = payload.message.substr(6);
            if (!checkLobby(target) && !checkSpec(target)) return;
            lobby.promoteHost(target);
        }
    }
    else if (payload.message.startsWith("/skip")) {
        if (!quiz.inQuiz) return;
        quiz.skipClicked();
    }
    else if (payload.message.startsWith("/lb")) {
        if (!quiz.inQuiz) return;
        if (!quiz.isHost) return;
        quiz.startReturnLobbyVote();
    }
    else if (payload.message.startsWith("/pause")) {
        if (!quiz.inQuiz) return;
        if (!quiz.isHost) return;
        if (quiz.pauseButton.pauseOn) {
            socket.sendCommand({
                type: "quiz",
                command: "quiz unpause",
            });
        } else {
            socket.sendCommand({
                type: "quiz",
                command: "quiz pause",
            });
        }
    }
    else if (payload.message.startsWith("/inv ")) {
        if (hostModal.gameMode === 'Ranked') return;
        if (!quiz.inQuiz && !lobby.inLobby) return;
        if (payload.message.length > 5) {
            socket.sendCommand({
                type: "social",
                command: "invite to game",
                data: {
                    target: payload.message.substr(5)
                }
            });
        }
    }
    else if (payload.message.startsWith("/autothrow")) {
        var index = payload.message.indexOf(' ');
        if (index > 0) autothrow = payload.message.substr(index + 1);
        else autothrow = '';
    }
}

let playNextSongListener = new Listener("play next song", payload => {
    if (quiz.isSpectator) return;
    setTimeout(function () {
        if (autothrow.length > 0) {
            quiz.skipClicked();
            $("#qpAnswerInput").val(autothrow);
            quiz.answerInput.submitAnswer(true);
        }
    }, 500);
}).bindListener();


function checkLobby(target) {
    if (!lobby.getPlayerByName(target)) return false;
    return true;
}
function checkSpec(target) {
    for (var user of gameChat.spectators) {
        if (user.name === target) return true;
    }
    return false;
}

function changeGameSettings(settings) {
    if (!settings) return;
    if (lobby.soloMode) {
        settings.roomSize = 1;
    }
    var settingChanges = {};
    Object.keys(settings).forEach((key) => {
        if (JSON.stringify(lobby.settings[key]) !== JSON.stringify(settings[key])) {
            settingChanges[key] = settings[key];
        }
    });
    if (Object.keys(settingChanges).length > 0) {
        hostModal.changeSettings(settingChanges);
        setTimeout(function () { lobby.changeGameSettings() }, 1);
    }
}

function AdjustVolume(amount) {
    var volumetemp = Cookies.get('volume') * 1;
    volumetemp = volumetemp + amount;
    volumetemp = Math.min(Math.max(volumetemp, 0), 1);
    volumeController.volume = volumetemp;
    volumeController.adjustVolume();
    volumeController.setMuted(false);
}
/* Nyamu userscript */


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

