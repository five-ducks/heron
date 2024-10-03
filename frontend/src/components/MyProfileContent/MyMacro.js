import { Component } from "../../core/core.js";
import { Input } from "../../components/Input.js";

export class MyMacro extends Component {
	constructor(props) {
		super({
			props: {
				className: 'my-macro',
			}
		});
		this.macroTextRender(props);
	}
	macroTextRender(macroText) {
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
			}, macroText[0]).el);
		this.el.querySelector('.f2').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '400px',
				height: '60px',
				fontsize: '25px',
			}, macroText[1]).el);
		this.el.querySelector('.f3').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '400px',
				height: '60px',
				fontsize: '25px',
			}, macroText[2]).el);
		this.el.querySelector('.f4').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '400px',
				height: '60px',
				fontsize: '25px',
			}, macroText[3]).el);
		this.el.querySelector('.f5').appendChild(new Input(
			'', 'text', {
				background: "url('../../../public/images/ui/macro-input.png')",
				width: '400px',
				height: '60px',
				fontsize: '25px',
			}, macroText[4]).el);
	}
}