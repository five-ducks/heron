import { Component } from "../../core/core.js";
import { ProfileLevel } from "./ProfileLevel.js";
import { Button } from "../Button.js";

export class ProfileSummary extends Component {
	constructor() {
		super({
			props: {
				className: 'profile-summary',
			}
		});
	}

	render() {
		this.el.innerHTML = /*html*/`
			<div class="profile-summary-img"></div>
			<div class="vertical-line"></div>
			<div class="profile-summary-name">
				<span>USERNAME</span>
			</div>
			<div class="vertical-line"></div>
			<div class="profile-summary-win">
				<p>승부 요약</p>
				<span>1 대 1 : </span><span>99%</span>
				<br>
				<span>토너먼트 : </span> <span>99%</span>
			</div>
			<div class="vertical-line"></div>
			<div class="button-container"></div>
		`;

		//프로필 이미지
		const profileImg = this.el.querySelector('.profile-summary-img'); 
		const img = document.createElement('img');
		img.src = '../../../public/images/charactors/pikachu.png';
		profileImg.appendChild(img);

		//유저 이름 & 프로필 레벨
		const profileName = this.el.querySelector('.profile-summary-name'); 
		profileName.appendChild(new ProfileLevel().el);

		// 승부 요약
		const profileWin = this.el.querySelector('.profile-summary-win'); 

		const logoutBtn = new Button({
			width: '130px',
			height: '60px',
			size: '25px',
			background : "url('../../../public/images/ui/profile-button.png')",
		},
		'로그아웃',
		() => {
			// 로그아웃 로직
		}
		);
		const withdrawalBtn = new Button({
			width: '130px',
			height: '60px',
			size: '25px',
			background : "url('../../../public/images/ui/profile-button.png')",
		},
		'회원탈퇴',
		() => {
			// 회원 탈퇴 로직
		}
		);
		this.el.querySelector('.button-container').appendChild(logoutBtn.el);
		this.el.querySelector('.button-container').appendChild(withdrawalBtn.el);
	}
}
