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
			<div class="macro-input f1"><div class="macro-key-name">F1</div></div>
			<div class="macro-input f2"><div class="macro-key-name">F2</div></div>
			<div class="macro-input f3"><div class="macro-key-name">F3</div></div>
			<div class="macro-input f4"><div class="macro-key-name">F4</div></div>
			<div class="macro-input f5"><div class="macro-key-name">F5</div></div>
		`
		this.el.querySelector('.f1').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '400px',
				height: '60px',
				fontsize: '25px',
			}, 'Hi').el);
		this.el.querySelector('.f2').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '400px',
				height: '60px',
				fontsize: '25px',
			}, 'GG').el);
		this.el.querySelector('.f3').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '400px',
				height: '60px',
				fontsize: '25px',
			}, '좋은 게임이였습니다.').el);
		this.el.querySelector('.f4').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '400px',
				height: '60px',
				fontsize: '25px',
			}, 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋ').el);
		this.el.querySelector('.f5').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '400px',
				height: '60px',
				fontsize: '25px',
			}, ':)').el);
	}
}