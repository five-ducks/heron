import { Component } from "../../core/core.js";
import store from "../../store/game.js";
import { Outcome } from "./Outcome.js";

// 하나의 게임 결과
export class OneGameRecord extends Component {
	constructor() {
		super({
			props: {
				className: 'one-game-record',
			}
		});
	}
	render(gameRecord) {
		const myName = "Ava"; // 내 아이디 (임시)
		console.log(gameRecord);
		if (gameRecord) {
			const user1_name = gameRecord.user1_name;
			const user2_name = gameRecord.user2_name;
			const match_result = gameRecord.match_result;
			const match_time = gameRecord.match_end_time;
			let isWin = false; // 내가 이겼는지

			if (user1_name == myName) {
				if (match_result ==='user1_win') {
					isWin = true;
				}
			}
			else {
				if (match_result == 'user2_win') {
					isWin = true;
				}
			}

			let match_type = 'single';

			if (gameRecord.match_type === 'single') {
				match_type = '1 : 1';
			} else {
				match_type = '토너먼트';
			}

			this.el.innerHTML = /*html*/`
				<div class="game-type">${match_type}</div>
				<div class="left-user"></div>
				<span>VS</span>
				<div class="right-user"></div>
				<div class="match-time">${match_time}</div>
			`

			const leftUSer = this.el.querySelector('.left-user');
			const rightUser = this.el.querySelector('.right-user');
			const leftOutcome = new Outcome();
			const rightOutcome = new Outcome();
			leftOutcome.render(isWin, user1_name);
			rightOutcome.render(!isWin, user2_name);
			leftUSer.appendChild(leftOutcome.el);
			rightUser.appendChild(rightOutcome.el);
		}
	}
}
