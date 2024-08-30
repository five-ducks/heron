import { Component } from "../core/core.js"
import { Button } from "../components/Button.js";

export default class Home extends Component {
	render() {
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