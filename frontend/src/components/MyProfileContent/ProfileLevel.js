import { Component } from "../../core/core.js";

export class ProfileLevel extends Component {
	constructor(exp) {
		super({
			props : {
				className: 'profile-level',
			}
		});

		// 레벨을 exp 값으로 계산
		const level = this.calculateLevel(exp);
		let src = '';
		
		// 레벨에 따른 이미지 경로 설정
		if (level === 1) {
			src = '../../../public/images/level/lv1.png';
		} else {
			src = '../../../public/images/level/lv2.png';
		}

		// 렌더링
		this.render(level, src);
	}

	// exp 값을 이용하여 레벨을 계산하는 함수
	calculateLevel(exp) {
		const baseLevel = 1; // 기본 레벨 1
		const additionalLevels = Math.floor(exp / 1000); // 1000 exp 당 1 레벨 추가
		return baseLevel + additionalLevels;
	}

	render(level, src) {
		this.el.innerHTML = /*html*/`
			<div class="level">
				<img src=${src} alt="level">
				<span> LV </span>
				<span>${level}</span>
			</div>
		`;
	}
}