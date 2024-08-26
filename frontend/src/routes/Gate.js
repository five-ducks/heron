import { Component } from "../core/core.js"
import { Button } from "../components/Button.js";

export default class Home extends Component {
	render() {
		// this.el.innerHTML = /*html*/`
		// <div class="gate">
		// 	<div class="container text-center">
		// 		<div class="row">
		// 			<h1>42</h1>
		// 		</div>
		// 		<div class="row">
		// 			<h1>Ping Pong</h1>
		// 		</div>
		// 		<div class="row button-row">
		// 			<button>Login</button>
		// 		</div>
		// 	</div>
		// </div>
		// `
		// // CSS 스타일 추가
		// const style = document.createElement('style');
		// style.textContent = /*css*/`
		// 	.gate {
		// 		display: flex;
		// 		justify-content: center;
		// 		align-items: center;
		// 		height: 100vh;
		// 		background-image: url('./space_bg.png'); /* 배경 이미지 경로 */
		// 		background-size: cover; /* 이미지가 컨테이너에 맞게 조정됨 */
		// 		background-position: center; /* 이미지가 중앙에 위치함 */
		// 	}
		// 	.container {
		// 		text-align: center;
		// 	}
		// 	.row {
		// 		margin-bottom: 20px;
		// 	}
		// 	.button-row {
		// 		display: flex;
		// 		justify-content: center; /* 버튼을 가로로 중앙에 위치시킴 */
		// 	}
		// 	.loginbtn {
		// 		max-width: 150px; /* 버튼의 최대 너비 설정 */
		// 		width: 100%; /* 버튼이 부모 요소의 너비에 맞게 확장 */
		// 	}
		// `;
		// this.el.appendChild(style);

		this.el.innerHTML = /*html*/`
		<div class="gate">
			<div class="container text-center">
				<div class="row">
					<h1>42</h1>
					<h1>Ping Pong</h1>
				</div>
				<div class="button-row">
				</div>
			</div>
		</div>
		`

		const button = new Button(
			{},
			'Login',
			() => {
				location.href = '/#/login';
			}
		);	
		this.el.querySelector('.button-row').appendChild(button.el);
	}
}