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

		this.el.addEventListener('click', (event) => {
			event.stopPropagation(); // 모달 외부 클릭 무시
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
