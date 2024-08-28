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

		// store의 gameRecords 상태를 구독하고, 변경 시 렌더링
		store.subscribe('gameRecords', () => {
			this.render();
		});

		// 데이터가 로드되지 않은 경우에만 로드
		if (store.state.gameRecords.length === 0) {
			this.loadData();
		}
	}

	async loadData() {
		await loadGameRecords();
	}

	render() {
		this.el.innerHTML = /*html*/``;

		const gameRecords = store.state.gameRecords.gameRecords;
		console.log(gameRecords);
		if (gameRecords) {
			gameRecords.forEach(gameRecord=> {
				this.el.appendChild(new OneGameRecord(gameRecord).el);
			});
		}
	}
}
