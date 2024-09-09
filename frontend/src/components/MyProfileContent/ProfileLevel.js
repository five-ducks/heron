import { Component } from "../../core/core.js";

export class ProfileLevel extends Component {
	constructor(exp) {
		super({
			props : {
				className: 'profile-level',
			}
		});

		// 레벨 별 이미지 정하기
		console.log(exp) // 이 데이터를 이용해서 레벨을 계산
		const level = 1;
		let src = '';
		this.calculateLevel();
		if (level === 1) {
			src = '../../../public/images/level/lv1.png';
		} else {
			src = '../../../public/images/level/lv2.png';
		}
		this.render(level, src);
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
	calculateLevel() {}
}