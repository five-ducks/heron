import { Component } from "../core/core.js";

export class Button extends Component {
	constructor(style = {}, text = 'Button', onClick = () => {}) {
		super({
			tagName: 'button'
		});
		this.el.textContent = text;

		const {
			width = '426.67px',
			height = '246.25px',
			background = "url('../public/images/button.png')",
			color = 'white',
		} = style;

		this.el.style.width = width;
		this.el.style.height = height;
		this.el.style.backgroundImage = background;
		this.el.style.color = color;
		this.el.style.backgroundSize = 'cover';
		this.el.style.border = 'none';
		this.el.style.backgroundColor = 'transparent';
		this.render();
		this.el.addEventListener('click', onClick);
	}

	render() {
	}
}
