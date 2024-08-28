import { Component } from "../../core/core.js";

export class Outcome extends Component {
	render(isWin, userName) {
		this.el.innerHTML = /*html*/`
			<div class="profile-result-img"></div>
			<div class="result">
				${isWin ? 'WIN' : 'LOSE'}
		`
		const profileImg = this.el.querySelector('.profile-result-img'); 
		const img = document.createElement('img');
		img.src = '../../../public/images/charactors/pikachu.png';
		// 여기 userId로 이미지 찾는거 넣어야함
		// 지금은 임시 이미지
		profileImg.appendChild(img);
		const profileName =  document.createElement('span');
		// 여기 userId로 이름 찾는거 넣어야함
		// 지금은 임시 이름
		profileName.textContent = userName;
		profileImg.appendChild(profileName);
	}
}