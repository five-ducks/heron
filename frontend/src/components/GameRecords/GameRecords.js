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
		fetch('../../temp/gameRecords.json')
		.then(res => res.json())
		.then(data => {
			console.log(data);
		})
		.catch(error => {
			console.error('Error:', error);
		});
	}
}