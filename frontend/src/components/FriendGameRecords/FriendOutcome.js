import { Component } from "../../core/core.js";
import { Avatar } from "../Profile/Avatar.js";

export class Friendoutcome extends Component {
	constructor() {
		super({
			props: {
				className: 'outcome',
			}
		});
	}
	render(isWin, userName) {
		const result = isWin ? 'WIN' : 'LOSE';
		this.el.innerHTML = /*html*/`
			<div class="profile-container">
				<div class="profile-result-img"></div>
				<div class="user-name">${userName}</div>
			</div>
			<div class="result">
				${result}
			</div>
		`
		const profileImg = this.el.querySelector('.profile-result-img');
		const img = new Avatar(0, 'm');
		profileImg.appendChild(img.el);

		const resultEl = this.el.querySelector('.result');

		// 이겼으면 파란색, 졌으면 빨간색 텍스트 테두리를 설정
		if (isWin) {
            resultEl.style.textShadow = '-1px 1px 0px #0000ff, 1px -1px 0px #0000ff, -1px -1px 0px #0000ff, 1px 1px 0px #0000ff';
        } else {
            resultEl.style.textShadow = '-1px 1px 0px #ff0000, 1px -1px 0px #ff0000, -1px -1px 0px #ff0000, 1px 1px 0px #ff0000'; ;
        }
	}
}