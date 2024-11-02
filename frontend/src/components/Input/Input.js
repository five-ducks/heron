import { Component } from "../../core/core.js";

export class Input extends Component {
	constructor(props = {}) {
		super({
			props : {
				className: 'input-field',
			},
		});

		const {
			label = '',
			id = '',
			defaultValue = '',
			placeholder = '',
			type = 'text',
			variant = 'default',
			size = 'm',
		} = props;


		const labelEl = document.createElement('label');
		labelEl.textContent = label;
		labelEl.setAttribute('for', id);
		this.el.appendChild(labelEl);

		const inputEl = document.createElement('input');
		inputEl.setAttribute('id', id);
		inputEl.value = defaultValue;
		inputEl.setAttribute('placeholder', placeholder);
		inputEl.setAttribute('type', type);
		switch (variant) {
			case 'background':
				inputEl.classList.add('input-background');
				break;
			default:
				inputEl.classList.add('input-default');
		}
		switch (size) {
			case 's':
				labelEl.classList.add('label-small');
				inputEl.classList.add('input-small');
				break;
			case 'l':
				labelEl.classList.add('label-large');
				inputEl.classList.add('input-large');
				break;
			default :
				labelEl.classList.add('label-medium');
				inputEl.classList.add('input-medium');
		}
		this.el.appendChild(inputEl);
		this.render();
	}
	getValue() {
		return this.el.querySelector('input').value.trim();
	}

	setValue(value) {
		this.el.querySelector('input').value = value;
	}

	render() {
		// 추가적인 렌더링 로직이 필요할 경우 여기에 작성
	}
}
