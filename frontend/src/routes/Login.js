import { Component } from "../core/core.js"
import { Button } from "../components/Button.js";
import { JoinModal } from "../components/JoinModal/JoinModal.js";

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
		'JOIN', () => {
			joinModal.open();
			console.log('join')
		});

		this.el.querySelector('.button-row').append(loginButton.el, authButton.el, signUpButton.el);

		const joinModal = new JoinModal(() => {
			console.log('closed');
			// 모달 창 닫힐 때 처리할 내용
		});

		this.el.appendChild(joinModal.el);
	}
}
