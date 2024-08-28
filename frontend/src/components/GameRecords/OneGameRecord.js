import { Component } from "../../core/core.js";

// 하나의 게임 결과
export class OneGameRecord extends Component {
	constructor(gameResult) {
		super({
			props: {
				className: 'one-game-result',
			}
		});
		
		this.gameResult = gameResult;

		console.log(this.gameResult); // 전달된 gameResult 객체를 로그로 출력
	}

	render() {
	}
}
