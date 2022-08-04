// ==UserScript==
// @name         AMQ DMs Timestamps
// @namespace    https://github.com/xSardine
// @version      1.2
// @description  Adds timestamps to DMs
// @author       xSardine
// @match        https://animemusicquiz.com/*
// @grant        none
// @downloadURL  https://github.com/xSardine/AMQ-Stuff/raw/main/BetterDms/DMs_Timestamp.user.js
// @updateURL    https://github.com/xSardine/AMQ-Stuff/raw/main/BetterDms/DMs_Timestamp.user.js
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

ChatBox.prototype.writeMessage = function (sender, msg, emojis, allowHtml) {
	msg = passChatMessage(msg, emojis, allowHtml);
	let d = new Date();
	let mins = d.getMinutes() < 10 ? "0" + d.getMinutes() : d.getMinutes();
	let hours = d.getHours() < 10 ? "0" + d.getHours() : d.getHours();
	let timeFormat = hours + ":" + mins;
	let final = timeFormat + "> " + sender;
	let atBottom = this.$CHAT_CONTENT.scrollTop() + this.$CHAT_CONTENT.innerHeight() >= this.$CHAT_CONTENT[0].scrollHeight;
	this.$CHAT_CONTENT.append(format(chatBoxLineTemplate, msg, final));
	if (atBottom) {
		this.$CHAT_CONTENT.scrollTop(this.$CHAT_CONTENT.prop("scrollHeight"));
	}
	this.$CHAT_CONTENT.perfectScrollbar('update');
};

//Initialize listeners and 'Installed Userscripts' menu
function setup() {
	AMQ_addScriptData({
		name: "DMs Timestamps",
		author: "xSardine",
		description: `<p>Add the time at which the DM has been sent (Advised to use it along the <a href="https://github.com/xSardine/AMQ-Stuff/tree/main/BetterDms" target="_blank">Bigger DM userscript</a> or else it's kinda small)</p>
				<p><a href="https://github.com/xSardine/AMQ-Stuff/raw/main/BetterDms/DMs_Timestamp.user.js">Click this link</a> to update it.</p>`
	});
}

