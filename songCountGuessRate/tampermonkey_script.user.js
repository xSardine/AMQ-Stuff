// ==UserScript==
// @name         AMQ Song Play Count / Guess Rate
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Display the number of time this song played before and your guess rate on it in the song info window
// @author       xSardine
// @match        https://animemusicquiz.com/*
// @downloadURL  https://github.com/xSardine/AMQ-Stuff/raw/main/songCountGuessRate/tampermonkey_script.user.js
// @updateURL    https://github.com/xSardine/AMQ-Stuff/raw/main/songCountGuessRate/tampermonkey_script.user.js
// @grant        none
// @require      https://raw.githubusercontent.com/TheJoseph98/AMQ-Scripts/master/common/amqScriptInfo.js
// ==/UserScript==

/* global Listener */

const SERVER_ADDRESS = "http://localhost:8010"

var infoDiv;

if (window.quiz) {
    setup()
}

function isCorrect(data) {

    let myID = -1
    for (let player in window.quiz.players) {
        if (window.quiz.players[player].isSelf) {
            myID = window.quiz.players[player].gamePlayerId
        }
    }

    let isCorrect = false
    for (let player in data.players) {
        if (data.players[player].gamePlayerId == myID) {
            isCorrect = data.players[player].correct
        }
    }

    return isCorrect

}

function onSongPlayed(data) {


    let body = {
        "songName": data.songInfo.songName,
        "artist": data.songInfo.artist
    }

    let correct = isCorrect(data)

    body["isCorrect"] = correct
    body["isSpectator"] = quiz.isSpectator

    let params = {
        method: 'post',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    }

    fetch(`${SERVER_ADDRESS}/songrec`, params)
        .then(req => req.json())
        .then(res => {

            if (!res.inDatabase) {
                infoDiv.innerHTML = "First time encountered"
                return
            }

            let correctIncrement = 0
            if (correct) {
                correctIncrement = 1
            }

            let playCountIncrement = 0
            if (!quiz.isSpectator) {
                playCountIncrement = 1
            }

            if (!quiz.isSpectator || res.playCount > 0) {
                infoDiv.innerHTML = `Play Count: <b>${res.playCount + playCountIncrement}</b> (${Math.floor((res.correctCount + correctIncrement) / (res.playCount + playCountIncrement) * 100)}%)`;
                infoDiv.innerHTML += `<br>Last played: <b>${timeAgo(res.lastTimePlayed)}</b>`;
            }
        })
}

function setup() {
    var boxDiv = document.querySelector('div.qpSideContainer > div.row')
    infoDiv = document.createElement('div')

    infoDiv.className = "rowPlayCount"

    boxDiv = boxDiv.parentElement
    boxDiv.insertBefore(infoDiv, boxDiv.children[4])

    new Listener("answer results", onSongPlayed).bindListener()
}

function timeAgo(time) {

    switch (typeof time) {
        case 'number':
            break;
        case 'string':
            time = +new Date(time);
            break;
        case 'object':
            if (time.constructor === Date) time = time.getTime();
            break;
        default:
            time = +new Date();
    }
    var time_formats = [
        [60, 'seconds', 1], // 60
        [120, '1 minute ago', '1 minute from now'], // 60*2
        [3600, 'minutes', 60], // 60*60, 60
        [7200, '1 hour ago', '1 hour from now'], // 60*60*2
        [86400, 'hours', 3600], // 60*60*24, 60*60
        [172800, 'Yesterday', 'Tomorrow'], // 60*60*24*2
        [604800, 'days', 86400], // 60*60*24*7, 60*60*24
        [1209600, 'Last week', 'Next week'], // 60*60*24*7*4*2
        [2419200, 'weeks', 604800], // 60*60*24*7*4, 60*60*24*7
        [4838400, 'Last month', 'Next month'], // 60*60*24*7*4*2
        [29030400, 'months', 2419200], // 60*60*24*7*4*12, 60*60*24*7*4
        [58060800, 'Last year', 'Next year'], // 60*60*24*7*4*12*2
        [2903040000, 'years', 29030400], // 60*60*24*7*4*12*100, 60*60*24*7*4*12
        [5806080000, 'Last century', 'Next century'], // 60*60*24*7*4*12*100*2
        [58060800000, 'centuries', 2903040000] // 60*60*24*7*4*12*100*20, 60*60*24*7*4*12*100
    ];
    var seconds = (+new Date() - time) / 1000,
        token = 'ago',
        list_choice = 1;

    if (seconds == 0) {
        return 'Just now'
    }
    if (seconds < 0) {
        seconds = Math.abs(seconds);
        token = 'from now';
        list_choice = 2;
    }
    var i = 0,
        format;
    while (format = time_formats[i++]) {
        if (seconds < format[0]) {
            if (typeof format[2] == 'string') {
                return format[list_choice];
            } else {
                return Math.floor(seconds / format[2]) + ' ' + format[1] + ' ' + token;
            }
        }
    }
    return time;
}

AMQ_addScriptData({
	name: "AMQ Song Play Count / Guess Rate",
	author: "xSardine",
	description: `Display the number of time this song played before and your guess rate on it in the song info window`
});
