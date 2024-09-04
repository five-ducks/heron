import { Component } from "../../core/core.js";
import { ProfileSummary } from "./ProfileSummary.js";
import { MyMacro } from "./MyMacro.js";
import { GameRecords } from "../GameRecords/GameRecords.js";

export class MyProfileContent extends Component {
	constructor() {
		super({
			props: {
				className: 'my-profile-content',
			}
		});
	}
	render() {
		this.el.innerHTML = /*html*/`
		`
		this.el.appendChild(new ProfileSummary().el);

		const horizontalLine = document.createElement('div');
		horizontalLine.className = 'horizontal-line';
		this.el.appendChild(horizontalLine);

		const macroAndRecords = document.createElement('div');
		macroAndRecords.className = 'macro-and-records';
		macroAndRecords.appendChild(new MyMacro().el);
		macroAndRecords.appendChild(new GameRecords().el);

		this.el.appendChild(macroAndRecords);
	}
}