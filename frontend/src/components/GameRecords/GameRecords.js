import { Component } from "../../core/core.js";
import { OneGameRecord } from "./OneGameRecord.js";
import store, { loadGameRecords } from "../../store/game.js"; 

// 전적 영역
export class GameRecords extends Component {
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
				const oneGameRecord = new OneGameRecord();
				oneGameRecord.render(gameRecord);
				this.el.appendChild(oneGameRecord.el);
			});
		}
	}
}
