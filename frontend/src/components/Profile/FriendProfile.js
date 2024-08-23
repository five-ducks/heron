import { Component } from "../../core/core.js";

export class FriendProfile extends Component {
    constructor(nick = 'unknown', image = "../public/images/charactors/pikachu.png", onSelect = () => {}) {
		super({
			tagName: 'button'
		});
		const src = image;
		const img = document.createElement('img');
		img.src = src;

		const frame = document.createElement('div');
		frame.classList.add('frame');
		this.el.appendChild(frame);
		frame.appendChild(img);
		
		const span = document.createElement('span');
		span.textContent = nick;
		this.el.appendChild(span);

		this.isSelected = false;
		this.el.addEventListener('click', () => {
			onSelect(this);
		});

		this.render();
	}

	render() {
        this.el.classList.add('charactor-profile');
	}
}