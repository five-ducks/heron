import { Component } from "../../core/core.js";
import store from "../../store/game.js";
import { Friendoutcome } from "./FriendOutcome.js";

// 하나의 게임 결과
export class FriendOneGameRecord extends Component {
	constructor() {
		super({
			props: {
				className: 'friend-one-game-record',
			}
		});
	}
	render(gameRecord, name) {
		const myName = name;
		if (gameRecord) {
			const user1_name = gameRecord.user1_name;
			const user2_name = gameRecord.user2_name;
			const user1_profile_img = gameRecord.user1_profile_img;
			const user2_profile_img = gameRecord.user2_profile_img;
			const match_result = gameRecord.match_result;
			const match_time = new Date(gameRecord.match_end_time);
			const user1IsWin = ( match_result === 'user1_win');
			const user2IsWin = ( match_result === 'user2_win');
			let isWin; // 내가 이겼는지 졌는지
			let enemy;
			let enemypic;
			if (user1_name === myName) {
				isWin = user1IsWin;
				enemy = user2_name;
				enemypic = user2_profile_img;
			} else {
				isWin = user2IsWin;
				enemy = user1_name;
				enemypic = user1_profile_img;
			}

			// 날짜와 시간 포맷 지정
			const year = match_time.getFullYear();
			const month = String(match_time.getMonth() + 1).padStart(2, '0'); // 월은 0부터 시작하므로 +1 필요
			const day = String(match_time.getDate()).padStart(2, '0');
			const hours = String(match_time.getHours()).padStart(2, '0');
			const minutes = String(match_time.getMinutes()).padStart(2, '0');

			// 형식에 맞게 날짜와 시간 결합
			const formattedDateTime = `${year}/${month}/${day}<br>${hours}:${minutes}`;
			let match_type = 'single';

			if (gameRecord.match_type === 'single') {
				match_type = '1 : 1';
			} else {
				match_type = '토너먼트';
			}

			this.el.innerHTML = /*html*/`
				<div class="game-type">${match_type}</div>
				<div class="left-user"></div>
				<div class="match-time">${formattedDateTime}</div>
			`

			const leftUSer = this.el.querySelector('.left-user');
			const leftOutcome = new Friendoutcome();
			leftOutcome.render(isWin, enemy, enemypic);
			leftUSer.appendChild(leftOutcome.el);

			if (isWin) {
				this.el.style.backgroundImage = "url('../../../public/images/win-bg.png')";
			} else {
				this.el.style.backgroundImage = "url('../../../public/images/lose-bg.png')";
			}
		}
	}
}
