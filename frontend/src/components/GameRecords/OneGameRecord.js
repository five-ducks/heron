import { Component } from "../../core/core.js";
import { Outcome } from "./Outcome.js";
import store from "../../store/game.js";

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
		const myName = store.state.userInfo.username;
		if (gameRecord) {
			const user1_name = gameRecord.user1_name;
			const user2_name = gameRecord.user2_name;
			const user1_profile_img = gameRecord.user1_profile_img;
			const user2_profile_img = gameRecord.user2_profile_img;
			const match_result = gameRecord.match_result;
			const match_time = new Date(gameRecord.match_end_time);
			const user1IsWin = (match_result === 'user1_win');
			const user2IsWin = (match_result === 'user2_win');
			let isWin; // 내가 이겼는지 졌는지
			if (user1_name === myName) {
				isWin = user1IsWin;
			}
			if (user2_name === myName) {
				isWin = user2IsWin;
			}

			// 날짜와 시간 포맷 지정
			const year = match_time.getFullYear();
			const month = String(match_time.getMonth() + 1).padStart(2, '0'); // 월은 0부터 시작하므로 +1 필요
			const day = String(match_time.getDate()).padStart(2, '0');
			const hours = String(match_time.getHours()).padStart(2, '0');
			const minutes = String(match_time.getMinutes()).padStart(2, '0');

			// 형식에 맞게 날짜와 시간 결합
			const formattedDateTime = `${year}/${month}/${day}<br>${hours}:${minutes}`;
			let match_type = 'onetoone';

			if (gameRecord.match_type === 'onetoone') {
				match_type = '1 : 1';
			} else {
				match_type = '토너먼트';
			}

			this.el.innerHTML = /*html*/`
				<div class="game-type">${match_type}</div>
				<div class="left-user"></div>
				<div class="vs-text">VS</div>
				<div class="right-user"></div>
				<div class="match-time">${formattedDateTime}</div>
			`

			const leftUSer = this.el.querySelector('.left-user');
			const rightUser = this.el.querySelector('.right-user');
			const leftOutcome = new Outcome();
			const rightOutcome = new Outcome();
			leftOutcome.render(user1IsWin, user1_name, user1_profile_img);
			rightOutcome.render(user2IsWin, user2_name, user2_profile_img);
			leftUSer.appendChild(leftOutcome.el);
			rightUser.appendChild(rightOutcome.el);

			if (isWin) {
				this.el.style.backgroundImage = "url('../../../public/images/win-bg.png')";
			} else {
				this.el.style.backgroundImage = "url('../../../public/images/lose-bg.png')";
			}
		}
	}
}
