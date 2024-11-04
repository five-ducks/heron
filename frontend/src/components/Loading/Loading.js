import { Component } from "../../core/core.js";

export class Loading extends Component {
	constructor() {
		super({
			props: {
				className: 'loading-screen',
			}
		});
	}
	render() {
		const img = document.createElement('img');
		img.src = '../../public/loading/loading.gif';
		this.el.appendChild(img);

		const loadingText = document.createElement('div');
		loadingText.className = 'loading-text';
		loadingText.innerText = '로딩 중...';
		this.el.appendChild(loadingText);

		const livingPoint = document.createElement('div');
		livingPoint.className = 'living-point';
		this.el.appendChild(livingPoint);

		this.el.style.display = 'none';
		document.body.appendChild(this.el);
	}

	show() {
		this.el.style.display = 'flex';
	}

	remove() {
		this.el.remove();
	}
}