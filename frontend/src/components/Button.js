import { Component } from "../core/core.js";

export class Button extends Component {
	constructor({ style = 'gray', size = 'md', text = 'Button' }, onClick = () => { }) {
		super({
			tagName: 'button',
			props: {
				// Bootstrap 클래스로 변경
				// btn-primary는 기본 스타일, btn-md는 중간 크기를 나타냅니다.
				className: `btn-${style} btn-${size} btn`
			}
		});
		this.el.textContent = text;

		this.render();
		this.el.addEventListener('click', onClick);
	}

	setText(text) {
		this.el.textContent = text;
	}

	render() {
		// Bootstrap은 추가 렌더링 로직이 필요 없으므로 이 메서드는 비워둘 수 있습니다.
	}
}