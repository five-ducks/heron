import { Component } from "../../core/core.js";
import { ProfileSummary } from "./ProfileSummary.js";
import { MyMacro } from "./MyMacro.js";
import { GameRecords } from "../GameRecords/GameRecords.js";
import store, { loadUserInfo } from "../../store/game.js";

export class MyProfileContent extends Component {
	constructor() {
		super({
			props: {
				className: 'my-profile-content',
			}
		});
	}
	async render() {
		await loadUserInfo();
		console.log(store.state.userInfo);
		this.el.innerHTML = /*html*/`
		`;
		this.el.appendChild(new ProfileSummary(store.state.userInfo).el);

		const horizontalLine = document.createElement('div');
		horizontalLine.className = 'horizontal-line';
		this.el.appendChild(horizontalLine);

		const macroAndRecords = document.createElement('div');
		macroAndRecords.className = 'macro-and-records';
		macroAndRecords.appendChild(new MyMacro(store.state.userInfo.macrotext).el);
		macroAndRecords.appendChild(new GameRecords().el);

		this.el.appendChild(macroAndRecords);
	}
}