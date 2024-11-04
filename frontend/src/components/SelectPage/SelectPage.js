import { Component } from "../../core/core.js";
import { Loading } from "../Loading/Loading.js";

export class SelectPage extends Component {
	constructor() {
		super({
			props: {
				className: 'selectpage',
			}
		});
		this.loading = new Loading();
	}
	async fakeLoadingProcess() {
		// 실제 게임 로딩 과정
		// 현재는 2초간 대기하는 것으로 대체
		return new Promise(resolve => setTimeout(resolve, 2000));
	}

	render() {
		this.el.innerHTML = /*html*/`
			<h1>게임 선택</h1>
			<div class="game-list">
				<button class="one-on-one">일대일</button>
				<button class="tournament">토너먼트</button>
			</div>
		`;

		this.el.querySelector('.one-on-one').addEventListener('click', async () => {
			this.loading.show();
			await this.fakeLoadingProcess();
			this.loading.remove();
		});
	}
}