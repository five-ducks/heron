import { Component } from "../core/core.js"
import { Button } from "../components/Button.js";
import { JoinModal } from "../components/JoinModal/JoinModal.js";
import { Input } from "../components/Input.js";

export default class Login extends Component {
	render() {
		this.el.innerHTML = /*html*/`
		<div class="login">
			<div class="container text-center">
				<div class="row">
					<h1>login</h1>
				</div>
				<div class="inputLogin">
					<div class="input_row" id="input_ID">
						<div class="input_label"> ID </div>
					</div>
					<div class="input_row" id="input_PW">
						<div class="input_label"> PW </div>
					</div>
				</div>
				<div class="button-row">
				</div>
				<div class="button-row">
				</div>
			</div>
		</div>
		`
		const input_ID = new Input(' Your Nickname!', 'text',
			{
				width: '440px',
				height: '80px'
			}
		);
		const input_PW = new Input(' ****', 'password',
			{
				width: '440px',
				height: '80px'
			}
		);

		const loginButton = new Button(
			{ 
				background: "url('../public/images/button.png')",
				width: '300px',
				height: '169px',
				size: '70px'
			},
			'Login',
			() => { console.log('login') }
		);
		const authButton = new Button(
			{ 
				background: "url('../public/images/button.png')",
				width: '300px',
				height: '169px',
				size: '70px', 
			},
			'42 Auth', 
			() => {	console.log('42 auth') }
		);
		const signUpButton = new Button(
			{
				background: "url('../public/images/button.png')",
				width: '300px',
				height: '169px',
				size: '70px',
			},
			'JOIN',
			() => {	
				joinModal.open();
				console.log('join')
			}
		);
		input_ID.el.classList.add('input_field');
		input_PW.el.classList.add('input_field');
		this.el.querySelector('#input_ID').append(input_ID.el);
		this.el.querySelector('#input_PW').append(input_PW.el);
		this.el.querySelector('.button-row').append(loginButton.el, authButton.el, signUpButton.el);

		const joinModal = new JoinModal(() => {
			console.log('closed');
			// 모달 창 닫힐 때 처리할 내용
		});
		this.el.appendChild(joinModal.el);
	}
}
