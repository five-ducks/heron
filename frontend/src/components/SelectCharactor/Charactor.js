import { Component } from "../../core/core.js";

export class Charactor extends Component {
	constructor(style = {}, name = "unknown", onSelect = () => { }) {
		super({
			tagName: 'button',
			props: {
				className: 'charactor'
			}
		});

		const {
			src = "../public/images/charactors/pikachu.png",
		} = style;

		const img = document.createElement('img');
		img.src = src;

		this.el.appendChild(img);

		const span = document.createElement('span');
		span.textContent = name;
		this.el.appendChild(span);

		this.isSelected = false;
		this.el.addEventListener('click', () => {
			onSelect(this);
		});

		this.render();
	}

	select() {
		this.isSelected = true;
		this.el.classList.add('selected');
	}

	deselect() {
		this.isSelected = false;
		this.el.classList.remove('selected');
	}

	render() {
	}
}
