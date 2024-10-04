import { Component } from "../core/core.js"
import { Button } from "../components/Button.js";

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