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

	render(record, name) {
		this.el.innerHTML = /*html*/``;

		if (record) {
			record.forEach(gameRecord => {
				const oneGameRecord = new FriendOneGameRecord();
				oneGameRecord.render(gameRecord, name);
				this.el.appendChild(oneGameRecord.el);
			});
		}
	}
}
