import { Component } from "../../core/core.js";
import { Loading } from "../Loading/Loading.js";
import { Button } from "../Button.js";

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
		return new Promise(resolve => setTimeout(resolve, 8000));
	}

	render() {
		this.el.classList.add('selectpage');
		this.el.classList.add('container');
		this.el.innerHTML = /*html*/`
			<h1>게임 선택</h1>
			<div class="game-list row">
				<!-- 각 버튼이 들어갈 자리 -->
			</div>
		`;

		// 일대일 버튼 생성 및 추가
		const oneToOneButton = new Button({
			text: '일대일',
			style: 'one-to-one',
			size: 'lg',
		});
		const gameList = this.el.querySelector('.game-list');

		gameList.appendChild(oneToOneButton.el);

		// 토너먼트 버튼 생성 및 추가
		const tournamentButton = new Button({
			text: '토너먼트',
			style: 'tournament',
			size: 'lg'
		});
		gameList.appendChild(tournamentButton.el);

		// 밍키리가 생성한 로딩, 교체 요망
		// this.el.querySelector('.one-to-one').addEventListener('click', async () => {
		// 	this.loading.show();
		// 	await this.fakeLoadingProcess();
		// 	this.loading.remove();
		// });

		// 1:1 게임 버튼 event listener
        const onetooneButton = this.el.querySelector('.btn-one-to-one');
        onetooneButton.addEventListener('click', () => {
            window.location.hash = '/game/onetoone/';
        });

		// 미구현 및 에러 방지를 위해 주석 처리
		// 토너먼트 게임 버튼 event listener
        // const tournamentButton = this.el.querySelector('.tournament');
    	// tournamentButton.addEventListener('click', () => {
        //     window.location.hash = '/game/tournament/';
        // });
	}
}