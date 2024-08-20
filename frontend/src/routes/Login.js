import { Component } from "../core/core.js"
import { Button } from "../components/Button.js";

export default class Login extends Component {
	render() {
		this.el.innerHTML = /*html*/`
		<div class="login">
			<div class="container text-center">
				<div class="row">
					<h1>Login</h1>
				</div>
				<div class="input_row">
					<input type="text" placeholder="ID">
				</div>
				<div class="input_row">
					<input type="password" placeholder="Password">
				</div>
				<div class="button-row">
				</div>
			</div>
		</div>
		`

		const loginButton = new Button(
			{ background: "url('../public/images/button.png')",
		width: '300px',
		height: '169px',
		size: '70px',},
		'Login',
		() => {
			console.log('login')
		});
		const authButton = new Button({ 
			background: "url('../public/images/button.png')",
			width: '300px',
			height: '169px',
			size: '70px', },
		'42 Auth', 
		() => {
			console.log('42 auth')
		});
		const signUpButton = new Button({ background: "url('../public/images/button.png')",
		width: '300px',
		height: '169px',
		size: '70px',},
		'Sign Up', () => {
			console.log('sign up')
		});

		this.el.querySelector('.button-row').append(loginButton.el, authButton.el, signUpButton.el);
		// // CSS 스타일 추가
		// const style = document.createElement('style');
		// style.textContent = /*css*/`
			// .login {
			// 	display: flex;
			// 	justify-content: center;
			// 	align-items: center;
			// 	height: 100vh;
			// 	background-image: url('./guggi.jpg'); /* 배경 이미지 경로 */
			// 	background-size: cover; /* 이미지가 컨테이너에 맞게 조정됨 */
			// 	background-position: center; /* 이미지가 중앙에 위치함 */
			// 	background-repeat: no-repeat; /* 배경 이미지 반복 방지 */
			// 	background-attachment: fixed; /* 배경 이미지가 스크롤하지 않도록 고정 */
			// }
		// 	.container {
		// 		text-align: center;
		// 	}
		// 	.row {
		// 		margin-bottom: 20px;
		// 	}
		// 	.input_row {
		// 		display: flex;
		// 		justify-content: center; /* input을 가로로 중앙에 배치 */
		// 		align-items: center; /* input을 세로로 중앙에 배치 */
		// 		margin-bottom: 20px; /* input 필드들 사이의 간격 */
		// 	}
		// 	.input_row input {
		// 		max-width: 300px; /* input의 최대 너비 */
		// 		width: 100%; /* input이 부모 요소의 너비에 맞게 확장 */
		// 		padding: 10px; /* input 내부 패딩 조정 */
		// 		box-sizing: border-box; /* padding 포함한 전체 크기를 설정 */
		// 	}
		// 	.button-row {
		// 		display: flex;
		// 		justify-content: center; /* 버튼들을 가로로 중앙에 배치 */
		// 		gap: 10px; /* 버튼들 간에 간격 추가 */
		// 	}
		// 	.loginbtn {
		// 		max-width: 100px; /* 버튼의 최대 너비를 100px로 설정 */
		// 		width: 100%; /* 버튼이 부모 요소의 너비에 맞게 확장 */
		// 		flex: 1; /* 버튼들이 동일한 너비를 가지도록 설정 */
		// 		padding: 10px 0; /* 버튼 내부 패딩 조정 */
		// 	}
		// `;
		// this.el.appendChild(style);
	}
}
