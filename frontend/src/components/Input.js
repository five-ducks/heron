import { Component } from "../core/core.js";

export class Input extends Component {
	constructor(placeholder = 'Input', type = 'text', style = {}, defaultValue = '', label = '', id = '') {
		super({
			props : {
				className: 'input-field',
			},
		});

		// 디폴트 스타일 설정
		const {
			width = '440px',
			height = '80px',
			background = "url('../public/images/input.png')",
			backgroundSize = 'cover',
			backgroundPosition = 'center',
			fontfamily = 'DungGeunMo',
			fontsize = '30px',
			marginBottom = '0px',
		} = style;

		console.log('label', label);
		console.log('id', id);
		// input 엘리먼트 생성
		const labelEl = document.createElement('label');
		if (label !== '') {
			labelEl.textContent = label;
		}
		if (id !== '') {
			labelEl.setAttribute('for', id);
		}
		this.el.appendChild(labelEl);

		const inputEl = document.createElement('input');

		// 스타일 적용
		inputEl.style.width = width;
		inputEl.style.height = height;
		inputEl.style.background = background; // 배경 색상과 이미지 조합
		inputEl.style.backgroundSize = backgroundSize;
		inputEl.style.backgroundPosition = backgroundPosition;
		inputEl.style.fontFamily = fontfamily;
		inputEl.style.fontSize = fontsize;
		inputEl.style.marginBottom = marginBottom;

		// placeholder 및 type 설정
		if (id !== '') {
			inputEl.setAttribute('id', id);
		}
		if (defaultValue !== '') {
			inputEl.value = defaultValue;
		}
		if (placeholder !== 'Input') {
			inputEl.setAttribute('placeholder', placeholder);
		}
		inputEl.setAttribute('type', type);
		this.el.appendChild(inputEl);
		this.render();
	}
	// value getter
	getValue() {
		return this.inputEl.value.trim();
	}

	// value setter
	setValue(value) {
		this.inputEl.value = value;
	}

	render() {
		// 추가적인 렌더링 로직이 필요할 경우 여기에 작성
	}
}
