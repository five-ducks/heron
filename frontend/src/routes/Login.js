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
	}
}
