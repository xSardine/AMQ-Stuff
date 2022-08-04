// ==UserScript==
// @name         AMQ 1 Second Audio
// @namespace    http://tampermonkey.net/
// @version      1.3
// @description  Mute the audio after 1s (can change timing by modifying delayBeforeMute variable)
// @author       xSardine
// @match        https://animemusicquiz.com/*
// @grant        none
// @copyright    MIT license
// @downloadURL  https://github.com/xSardine/AMQ-Stuff/raw/main/1SecondAudio/1Second_Audio.user.js
// @updateURL    https://github.com/xSardine/AMQ-Stuff/raw/main/1SecondAudio/1Second_Audio.user.js
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

"use strict"
let songStartTime = 0;
let songMuteTime = 0;
let muteClick;
let buzzerInitialized = false;

let toggled_ON = false

// Delay before audio mute itself (1s = 1000)
let delayBeforeMute = 1200

function notifyAutoReady() {
	if (quiz.gameMode === "Ranked") return;
	gameChat.systemMessage(toggled_ON ? "1s Automute is enabled. Press [ALT+M] to disable." : "1s Automute is Disabled. Press [ALT+M] to enable.");
}

function dockeyup(event) {
	if (event.altKey && event.keyCode == 77) {
		toggled_ON = !toggled_ON;
		console.log("Automute: toggle ", toggled_ON);

		// post enabled/disabled message to chat
		let message = toggled_ON ? "Enabled Automute" : "Disabled Automute";
		gameChat.systemMessage(message);
	}
}

function setupMuteBuzzer() {
	muteClick = document.getElementById("qpVolumeIcon");

	muteClick.observer = new MutationObserver((change) => {
		if (songMuteTime == "Unmuted") { null; }
		else {
			songMuteTime === 0 ? songMuteTime = Date.now() : songMuteTime = "Unmuted";
		}
	})

	if (muteClick.className === "fa fa-volume-off") { muteClick.click() };

	muteClick.observer.observe(muteClick, { attributes: true })
	songMuteTime = 0;
	buzzerInitialized = true;
}

// reset volume button between games
function shutdownBtn() {
	muteClick ? muteClick.observer.disconnect() : null;
	muteClick = null;
	buzzerInitialized = false;
	songMuteTime = 0;
}


function delayedMute() {
	muteClick.click()
}

//Initialize listeners and 'Installed Userscripts' menu
function setup() {

	// post to chat
	new Listener("answer results", (results) => {
		// post time in chat
		let songNumber = parseInt($("#qpCurrentSongCount").text());
		let message = "";

		if (toggled_ON && songMuteTime == "Unmuted") { message += "Player unmuted - disqualified" } // set unmuted message

		// post message to chat
		if (quiz.gameMode !== "Ranked") {
			let oldMessage = gameChat.$chatInputField.val();
			gameChat.$chatInputField.val(message);
			gameChat.sendMessage();
			gameChat.$chatInputField.val(oldMessage);
		}

		// reset for next round
		songMuteTime = 0;
	}).bindListener()

	new Listener("play next song", () => {
		if (!buzzerInitialized) { setupMuteBuzzer(); } // just in case
		if (muteClick.className === "fa fa-volume-off") { muteClick.click() }; // check if muted

		muteClick.observer.observe(muteClick, { attributes: true });

		songStartTime = Date.now();
		songMuteTime = 0;

		if (toggled_ON) {
			setTimeout(delayedMute, delayBeforeMute);
		}

	}).bindListener()


	// check exits
	new Listener("return lobby vote result", (result) => {
		if (result.passed) {
			shutdownBtn();
		}
	}).bindListener()
	// find mute button
	new Listener("Game Starting", (data) => {
		shutdownBtn();
		setupMuteBuzzer();
	}).bindListener()

	new Listener("rejoin game", (data) => {
		notifyAutoReady();
		shutdownBtn();
		setupMuteBuzzer();
		if (data) { songStartTime = Date.now(); }
	}).bindListener()
	// unmute and stop looking at mute button
	new Listener("guess phase over", () => {
		muteClick.observer.disconnect();
		if (muteClick.className === "fa fa-volume-off") { muteClick.click() };
	}).bindListener()
	new Listener("quiz over", () => {
		shutdownBtn();
	}).bindListener()
	new Listener("leave game", () => {
		shutdownBtn();
	}).bindListener()
	new Listener("Spectate Game", () => {
		notifyAutoReady();
		shutdownBtn();
	}).bindListener()
	new Listener("Join Game", (response) => {
		if (response.error) return;
		notifyAutoReady();
	}).bindListener();
	new Listener("Host Game", () => {
		notifyAutoReady();
		shutdownBtn();
	}).bindListener()
	document.addEventListener('keyup', dockeyup, false);

	AMQ_addScriptData({
		name: "1 Second Audio",
		author: "xSardine",
		description: `<p>Mute the audio after 1s (can change timing by modifying delayBeforeMute variable)</p>
			<p>Toggle ON/OFF: alt+m</p>
            <p><a href="https://github.com/xSardine/AMQ-Stuff/raw/main/1SecondAudio/1Second_Audio.user.js">Click this link</a> to update it.</p>`
	});

}


