import { Component } from "../../core/core.js";

// 하나의 게임 결과

export class OneGameResult extends Component {
	constructor() {
		super({
			props: {
				className: 'one-game-result',
			}
		});
	}

	render() {
		this.el.innerHTML = /*html*/`
		`
	}
}