import { Component } from "../core/core.js"
import { Button } from "../components/Button.js";
import { getSocketStatus } from "../status/status.js";

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
		let button;
		// 로그인 여부를 socket 을 통해 확인
		if (getSocketStatus()) {
			button = new Button({
				style: 'gray',
				size: 'l',
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
				size: 'l',
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