import { Component } from "../../core/core.js";
import { FriendOneGameRecord } from "./FriendOneGameRecord.js";
import store, { loadGameRecords } from "../../store/game.js"; 

// 전적 영역
export class FriendGameRecords extends Component {
	constructor() {
		super({
			props: {
				className: 'game-records',
			}
		});
	}

	async render() {
		// store에 저장된 게임 기록 불러오기,
		// 현재 하나의 record store를 여러 유저가 사용중,
		// 추가적인 공간을 준비 할 이유가 있는가 검토 필요

		await loadGameRecords();

		this.el.innerHTML = /*html*/``;

		const gameRecords = store.state.gameRecords.gameRecords;
		if (gameRecords) {
			gameRecords.forEach(gameRecord => {
				const oneGameRecord = new FriendOneGameRecord();
				oneGameRecord.render(gameRecord);
				this.el.appendChild(oneGameRecord.el);
			});
		}
	}
}
