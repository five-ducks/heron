import { Component } from "../../core/core.js";

export class Input extends Component {
	constructor(placeholder = '', variant='default', size='m', type = 'text', defaultValue = '', label = '', id = '') {
		super({
			props : {
				className: 'input-field',
			},
		});

		const labelEl = document.createElement('label');
		if (label !== '') {
			labelEl.textContent = label;
		}
		if (id !== '') {
			labelEl.setAttribute('for', id);
		}
		this.el.appendChild(labelEl);

		const inputEl = document.createElement('input');
		if (id !== '') {
			inputEl.setAttribute('id', id);
		}
		if (defaultValue !== '') {
			inputEl.value = defaultValue;
		}
		inputEl.setAttribute('placeholder', placeholder);
		inputEl.setAttribute('type', type);
		this.el.appendChild(inputEl);
		switch (variant) {
			case 'background':
				inputEl.classList.add('input-background');
				break;
			default:
				inputEl.classList.add('input-default');
		}

		switch (size) {
			case 's':
				inputEl.classList.add('small');
				break;
			case 'm':
				inputEl.classList.add('medium');
				break;
			case 'l':
				inputEl.classList.add('large');
				break;
		}
		this.render();
	}
	// value getter
	getValue() {
		return this.el.querySelector('input').value.trim();
	}

	// value setter
	setValue(value) {
		this.el.querySelector('input').value = value;
	}

	render() {
		// 추가적인 렌더링 로직이 필요할 경우 여기에 작성
	}
}
