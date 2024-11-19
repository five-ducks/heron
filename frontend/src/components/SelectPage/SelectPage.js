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
			<div class="game-list row justify-content-center">
				<!-- 각 버튼이 들어갈 자리 -->
			</div>
		`;

		// 일대일 버튼 생성 및 추가
		this.oneToOneButton = new Button({
			text: '일대일',
			style: 'one-to-one',
			size: 'lg',
		});

		const oneToOneCol = document.createElement('div');
		oneToOneCol.classList.add('col-auto');
		oneToOneCol.appendChild(this.oneToOneButton.el);
		this.el.querySelector('.game-list').appendChild(oneToOneCol);

		// 토너먼트 버튼 생성 및 추가
		this.tournamentButton = new Button({
			text: '토너먼트',
			style: 'tournament',
			size: 'lg'
		});

		const tournamentCol = document.createElement('div');
		tournamentCol.classList.add('col-auto');
		tournamentCol.appendChild(this.tournamentButton.el);
		this.el.querySelector('.game-list').appendChild(tournamentCol);

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

		// // 1:1 게임 버튼 event listener
        // const tournamentButton = this.el.querySelector('.tournament');
    	// tournamentButton.addEventListener('click', () => {
        //     window.location.hash = '/game/tournament/';
        // });
	}
}