import { Component } from "../../core/core.js";
import { OneGameRecord } from "./OneGameRecord.js";
import store, { loaduserGameRecords } from "../../store/game.js"; 

// 전적 영역
export class GameRecords extends Component {
	constructor() {
		super({
			props: {
				className: 'game-records row',
			}
		});
	}

	async render() {

		await loaduserGameRecords();

		this.el.innerHTML = /*html*/``;

		const gameRecords = store.state.userGameRecords;
		if (gameRecords) {
			gameRecords.forEach(gameRecord => {
				const oneGameRecord = new OneGameRecord();
				oneGameRecord.render(gameRecord);
				oneGameRecord.el.classList.add('col-12');
				this.el.appendChild(oneGameRecord.el);
			});
		}
		else {
			this.el.appendChild(document.createTextNode('게임 기록이 없습니다.'));
		}
	}
}
