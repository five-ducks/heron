import { Component } from "../../core/core.js";
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
		const myId = 1; // 내 아이디 (임시)
		console.log(gameRecord);
		if (gameRecord) {
			const match_type = gameRecord.match_type;
			const user1_id = gameRecord.user1_id;
			const user2_id = gameRecord.user2_id;
			const match_result = gameRecord.match_result;
			const match_time = gameRecord.match_end_time;
			let isWin = false; // 내가 이겼는지

			if (user1_id === myId) {
				if (match_result ==='user1_win') {
					isWin = true;
				}
			}
			else {
				if (match_result === 'user2_win') {
					isWin = true;
				}
			}

			this.el.innerHTML = /*html*/`
				<div class="game-type">${match_type}</div>
				<div class="my-result"></div>
				<div class="other-result"></div>
				<div class="match-time">${match_time}</div>
			`
		}
	}
}
