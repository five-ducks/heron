import { Component } from "../core/core.js";

export class Button extends Component {
	constructor({style = 'default', size = 'm', text = 'Button'}, onClick = () => {}) {
		super({
			tagName: 'button',
			props: {
				className: `${style} ${size}` // 기본값으로 style과 size 적용
			}
		});
		this.el.textContent = text;

		this.render();
		this.el.addEventListener('click', onClick);
	}

	render() {
		// 추가 렌더링 로직
	}
}



