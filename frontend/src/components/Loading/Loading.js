import { Component } from "../../core/core.js";
import { messages } from "../../store/messages.js";

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
		
		const livingPointText = document.createElement('p');
		livingPointText.innerText = '[리빙포인트]';
		livingPoint.appendChild(livingPointText);

		const livingPointContent = document.createElement('p');
		livingPointContent.innerText = '';
		livingPoint.appendChild(livingPointContent);

		this.el.style.display = 'none';
		document.body.appendChild(this.el);

		let Index = Math.floor(Math.random() * messages.length);
		livingPointContent.innerText = messages[Index];

		setTimeout(() => {
			this.messageInterval = setInterval(() => {
				Index = Math.floor(Math.random() * messages.length);
				livingPointContent.innerText = messages[Index];
			}, 4000);
		}, 4000);
	}

	show() {
		this.el.style.display = 'flex';
	}

	remove() {
		clearInterval(this.messageInterval);
		this.el.remove();
	}
}