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
			<div class="macro-input f1"><span>F1 : </span></div>
			<div class="macro-input f2"><span>F2 : </span></div>
			<div class="macro-input f3"><span>F3 : </span></div>
			<div class="macro-input f4"><span>F4 : </span></div>
			<div class="macro-input f5"><span>F5 : </span></div>
		`
		this.el.querySelector('.f1').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '320px',
				height: '50px',
			}, 'Hi').el);
		this.el.querySelector('.f2').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '320px',
				height: '50px',
			}, 'GG').el);
		this.el.querySelector('.f3').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '320px',
				height: '50px',
			}, '좋은 게임이였습니다.').el);
		this.el.querySelector('.f4').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '320px',
				height: '50px',
			}, 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋ').el);
		this.el.querySelector('.f5').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '320px',
				height: '50px',
			}, ':)').el);
	}
}