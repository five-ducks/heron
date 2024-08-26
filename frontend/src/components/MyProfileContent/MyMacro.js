import { Component } from "../../core/core.js";
import { Input } from "../../components/Input.js";

export class MyMacro extends Component {
	constructor() {
		super({
			props: {
				className: 'my-macro',
			}
		});
	}
	render() {
		this.el.innerHTML = /*html*/`
			<div class="macro-input f1">F1</div>
			<div class="macro-input f2">F2</div>
			<div class="macro-input f3">F3</div>
			<div class="macro-input f4">F4</div>
			<div class="macro-input f5">F5</div>
		`
		this.el.querySelector('.f1').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '320px',
				height: '50px',
			}, 'hi').el);
		this.el.querySelector('.f2').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '320px',
				height: '50px',
			}, 'hi').el);
		this.el.querySelector('.f3').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '320px',
				height: '50px',
			}, 'hi').el);
		this.el.querySelector('.f4').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '320px',
				height: '50px',
			}, 'hi').el);
		this.el.querySelector('.f5').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '320px',
				height: '50px',
			}, 'hi').el);
	}
}