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
		history.pushState(null, "", location.href);
		window.addEventListener("popstate", this.preventGoBack);
	}

	close() {
		this.el.style.display = 'none';
		window.removeEventListener("popstate", this.preventGoBack);
		this.onClose();
		this.el.remove();
	}

	preventGoBack() {
		history.go(1); 
	}
}
