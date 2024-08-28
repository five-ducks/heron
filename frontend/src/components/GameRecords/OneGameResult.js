import { Component } from "../../core/core.js";

// 하나의 게임 결과

export class OneGameResult extends Component {
	constructor(gameResult) {
		super({
			props: {
				className: 'one-game-result',
			}
		});
		this.gameResult = gameResult;
		console.log(this.gameResult);
	}

	render() {
		this.el.innerHTML = /*html*/`
		`
	}
}