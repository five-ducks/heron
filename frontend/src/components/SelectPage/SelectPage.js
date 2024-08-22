import { Component } from "../../core/core.js";

export class SelectPage extends Component {
	render() {
		this.el.classList.add('selectpage');
		this.el.innerHTML = /*html*/`
			<div class="contents">
				<div class="title">게임 선택</div>
				<div class="game-list">
					<button class="game">1 : 1</button>
					<button class="game">토너먼트</button>
				</div>
			</div>
		`;
	}
}