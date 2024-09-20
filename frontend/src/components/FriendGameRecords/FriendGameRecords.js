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
