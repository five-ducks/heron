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
		this.el.classList.add('selectpage');
		this.el.innerHTML = /*html*/`
			<h1>게임 선택</h1>
			<div class="game-list">
				<button class="one-to-one">일대일</button>
				<button class="tournament">토너먼트</button>
			</div>
		`;

		// 1:1 게임 버튼 event listener
        const onetooneButton = this.el.querySelector('.one-to-one');
        onetooneButton.addEventListener('click', () => {
            window.location.hash = '/game/onetoone/';
        });
	}
}