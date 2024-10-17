import { Component } from "../../core/core.js";

export class SelectPage extends Component {
	constructor() {
		super({
			props: {
				className: 'selectpage',
			}
		});
	}
	render() {
		this.el.innerHTML = /*html*/`
			<h1>게임 선택</h1>
			<div class="game-list">
				<button class="one-on-one">일대일</button>
				<button class="tournament">토너먼트</button>
			</div>
		`;
	}
}