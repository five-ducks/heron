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

	// 레벨당 필요한 exp 양 계산 함수
	static BASE_EXP = 1000; // 레벨당 기본 exp
	static EXP_MULTIPLIER = 1.5; // 레벨당 증가하는 exp 배율

	calculateLevel(exp) {
		let level = 1;
		let expForNextLevel = ProfileLevel.BASE_EXP; // 클래스 변수 접근 시 ProfileLevel 사용

		while (exp >= expForNextLevel) {
			exp -= expForNextLevel; // 다음 레벨로 가기 위해 필요한 exp 차감
			level++; // 레벨 업
			expForNextLevel = Math.floor(expForNextLevel * ProfileLevel.EXP_MULTIPLIER); // 다음 레벨에 필요한 exp 증가
		}

		return level;
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