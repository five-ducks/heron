import { Component } from "../../core/core.js";

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
		const img = document.createElement('img');
		img.src = '../../../public/images/charactors/pikachu.png';
		// 여기 userId로 이미지 찾는거 넣어야함
		// 지금은 임시 이미지
		profileImg.appendChild(img);

		const resultEl = this.el.querySelector('.result');

		// 이겼으면 파란색, 졌으면 빨간색 텍스트 테두리를 설정
		if (isWin) {
            resultEl.style.textShadow = '-1px 1px 0px #0000ff, 1px -1px 0px #0000ff, -1px -1px 0px #0000ff, 1px 1px 0px #0000ff';
        } else {
            resultEl.style.textShadow = '-1px 1px 0px #ff0000, 1px -1px 0px #ff0000, -1px -1px 0px #ff0000, 1px 1px 0px #ff0000'; ;
        }
	}
}