// ==UserScript==
// @name         AMQ Special Character Macro
// @namespace    https://github.com/xSardine
// @version      1.1
// @author       xSardine
// @description  press a key and @someone
// @match        https://animemusicquiz.com/*
// @grant        none
// @downloadURL  https://github.com/xSardine/AMQ-Stuff/raw/main/SpecialCharacterMacro/Special_Character_Macro.user.js
// @updateURL    https://github.com/xSardine/AMQ-Stuff/raw/main/SpecialCharacterMacro/Special_Character_Macro.user.js
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
