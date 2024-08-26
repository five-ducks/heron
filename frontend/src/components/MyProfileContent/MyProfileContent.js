import { Component } from "../../core/core.js";
import { ProfileSummary } from "./ProfileSummary.js";
import { MyMacro } from "./MyMacro.js";

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
			<span>내 프로필</span>
		`
		this.el.appendChild(new ProfileSummary().el);
		this.el.appendChild(new MyMacro().el);
	}
}