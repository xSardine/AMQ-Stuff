// ==UserScript==
// @name         Fast @
// @namespace    http://tampermonkey.net/
// @author       xSardine
// @description  press a key and @someone
// @match        https://animemusicquiz.com/*
// @grant        none
// ==/UserScript==




function doc_keyDown(event) {
    if (quiz.inQuiz || lobby.inLobby) {
        if ((event.keyCode == '97') && (event.ctrlKey)) {
            document.getElementById('gcInput').value += "@husahusahusahusa";
        }
        if (event.keyCode == '113') {
            if (quiz.answerInput.inFocus) {
                document.getElementById('qpAnswerInput').value += "ō";
            }
            else {
                document.getElementById('gcInput').value += "ō";
            }
        }
        if (event.keyCode == '115') {
            if (quiz.answerInput.inFocus) {
                document.getElementById('qpAnswerInput').value += "ū";
            }
            else {
                document.getElementById('gcInput').value += "ū";
            }
        }
    }
}

document.addEventListener('keydown', doc_keyDown, false);

function sendChatMessage(message) {
    gameChat.$chatInputField.val(message);
    gameChat.sendMessage();
}
