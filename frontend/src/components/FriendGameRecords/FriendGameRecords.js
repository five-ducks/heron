import { Component } from "../../core/core.js";
import { FriendOneGameRecord } from "./FriendOneGameRecord.js";
import store from "../../store/game.js";

export class FriendGameRecords extends Component {
	constructor() {
		super({
			props: {
				className: 'friend-game-records',
			}
		});
	}

	recoredsRender(name) {
		this.el.innerHTML = /*html*/``;

		const records = store.state.userFriendGameRecords[name];
		if (records) {
			records.forEach(gameRecord => {
				const oneGameRecord = new FriendOneGameRecord();
				oneGameRecord.render(gameRecord, name);
				this.el.appendChild(oneGameRecord.el);
			});
		}
	}
}