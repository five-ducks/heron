import { Component } from "../core/core.js"
import { Button } from "../components/Button.js";
import { getCookie } from "../core/core.js";

export default class Home extends Component {
	constructor() {
		super({
			props: {
				className: 'gate',
			}
		});
	}
	render() {
		this.el.innerHTML = /*html*/`
			<div class="logo">
			</div>
			<div class="button-row">
			</div>
		`;
		const player = getCookie('player');
		let button;
		// 로그인 되어있는지 세션 스토리지로 확인
		if (sessionStorage.getItem('isLoggedIn') === 'true') {
			button = new Button({
				style: 'gray',
				size: 'xxl',
				text: 'Start'
			},
				() => {
					location.href = '/#/main';
				}
			);
		}
		else {
			button = new Button({
				style: 'gray',
				size: 'xxl',
				text: 'Login'
			},
				() => {
					location.href = '/#/login';
				}
			);
		}
		this.el.querySelector('.button-row').appendChild(button.el);
	}
}