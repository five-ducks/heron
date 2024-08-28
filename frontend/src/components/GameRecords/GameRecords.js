import { Component } from "../../core/core.js";
import { OneGameResult } from "./OneGameResult.js";

// 전적 영역
export class GameRecords extends Component {
	constructor() {
		super({
			props: {
				className: 'game-records',
			}
		});
	}
	// 데이터 불러오기
	// 비동기로 수정
	async loadData() {
		try {
			const response = await fetch('https://localhost/src/temp/gameRecords.json');
			const data = await response.json();
			this.gameRecords = data.gameRecords;
			console.log('gameRecords:', this.gameRecords);
		} catch (error) {
			console.error('Error loading game records:', error);
		}
	}
	
	async render() {
		this.el.innerHTML = /*html*/`
		`

		// 데이터 불러오기까지 기다림
		await this.loadData();

		this.gameRecords.forEach(gameResult => {
			this.el.appendChild(new OneGameResult(gameResult).el);
		});
	}
}