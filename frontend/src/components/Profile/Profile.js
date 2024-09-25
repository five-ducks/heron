import { Component } from "../../core/core.js";
import { ProfileIcon } from "./ProfileIcon.js";

export class CharactorProfile extends Component {
    constructor(image = 1, name = "unknown", onSelect = () => {}) {
		super({
			tagName: 'button'
		});
		this.image = image;

		const img = new ProfileIcon(this.image);
		const frame = document.createElement('div');
		frame.classList.add('frame');
		this.el.appendChild(frame);
		frame.appendChild(img.el);

		const span = document.createElement('span');
		span.textContent = name;
		this.el.appendChild(span);

		this.isSelected = false;
		this.el.addEventListener('click', () => {onSelect(this);});

		this.render();
	}

	render() {
        this.el.classList.add('charactor-profile');
	}
}
