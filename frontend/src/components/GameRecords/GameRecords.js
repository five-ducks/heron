import { Component } from "../../core/core.js";

// 전적 영역
export class GameRecords extends Component {
	constructor() {
		super({
			props: {
				className: 'game-records',
			}
		});
		// 데이터 불러오기
		fetch('https://localhost/src/temp/gameRecords.json')
		.then(res => res.json())
		.then(gameRecords => {
			console.log(gameRecords);
		})
		.catch(error => {
			console.error('Error:', error);
		});
	}
}