import { Component } from "./core.js";

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
				<span class="close-button">&times;</span>
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
	}
}
