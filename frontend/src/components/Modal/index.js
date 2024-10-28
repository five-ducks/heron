import { Component } from "../../core/core.js";

export class Modal extends Component {
	constructor(title, content = '', onClose = () => { }) {
		super({
			tagName: 'div',
			props: {
				className: 'modal-overlay'
			}
		});
		this.el.innerHTML = /*html*/`
			<div class="modal-content">
				<div class="close-button"></div>
				<div class="modal-title">${title}</div>
				${content}
			</div>
		`;

		this.onClose = onClose;
		this.el.querySelector('.close-button').addEventListener('click', () => {
			this.close();
		});

		this.el.addEventListener('click', (event) => {
			event.stopPropagation();
		});

		this.el.querySelector('.modal-content').addEventListener('click', (event) => {
			event.stopPropagation();
		});
	}

	open() {
		this.el.style.display = 'block';
		document.body.style.pointerEvents = 'none';
		this.el.style.pointerEvents = 'auto';
		history.pushState(null, "", location.href);
		window.addEventListener("popstate", this.preventGoBack);
	}

	close() {
		this.el.style.display = 'none';
		document.body.style.pointerEvents = 'auto';
		window.removeEventListener("popstate", this.preventGoBack);
		this.onClose();
		this.el.remove();
	}

	preventGoBack() {
		history.go(1);
	}
}
