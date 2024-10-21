import { Component } from "../../core/core.js";
import { Profile } from "../Profile/Profile.js";

export class Friendoutcome extends Component {
	constructor() {
		super({
			props: {
				className: 'friendoutcome',
			}
		});
	}
	render(isWin, userName) {
		const result = isWin ? 'WIN' : 'LOSE';
		this.el.innerHTML = /*html*/`
			<div class="profile-container">
			</div>
			<div class="result">
				${result}
			</div>
		`;

		const profilecontainer = this.el.querySelector('.profile-container');
		const img = new Profile(0, userName, 's', { style: 'inner' });
		profilecontainer.appendChild(img.el);

		const resultEl = this.el.querySelector('.result');

		// 이겼으면 파란색, 졌으면 빨간색 텍스트 테두리를 설정
		if (isWin) {
            resultEl.style.textShadow = '-1px 1px 0px #0000ff, 1px -1px 0px #0000ff, -1px -1px 0px #0000ff, 1px 1px 0px #0000ff';
        } else {
            resultEl.style.textShadow = '-1px 1px 0px #ff0000, 1px -1px 0px #ff0000, -1px -1px 0px #ff0000, 1px 1px 0px #ff0000'; ;
        }
	}
}