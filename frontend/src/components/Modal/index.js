import { Component } from "../../core/core.js";

export class Modal extends Component {
	constructor(content = '', onClose = () => {}) {
		super({
			tagName: 'div',
			props: {
				className: 'modal'
			}
		});
		this.el.innerHTML = /*html*/`
			<div class="modal-content">
				<div class="close-button"></div>
				${content}
			</div>
		`;

		this.onClose = onClose;
		this.el.querySelector('.close-button').addEventListener('click', () => {
			this.close();
		});

		window.addEventListener('click', (event) => {
			if (event.target === this.el) {
				this.close();
			}
		});
	}

	open() {
		this.el.style.display = 'block';
	}

	close() {
		this.el.style.display = 'none';
		this.onClose();
		this.el.remove();
	}
}
