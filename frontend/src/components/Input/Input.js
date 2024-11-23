import { Component } from "../../core/core.js";

export class Input extends Component {
	constructor(props = {}) {
		super({
			props : {
				className: 'row align-items-center', // 변경: form-group에서 row align-items-center로
			},
		});

		const {
			label = 'none',
			labelPosition = 'top',
			id = '',
			defaultValue = '',
			placeholder = '',
			type = 'text',
			variant = 'default',
			size = 'm',
		} = props;

		// label에 값이 있는 경우에만 label 엘리먼트 추가
		const labelEl = document.createElement('label');
		if (label !== 'none') {
			labelEl.textContent = label;
			labelEl.setAttribute('for', id);
			labelEl.classList.add('col-form-label', 'fw-bold'); // fw-bold 클래스 추가
			if (labelPosition === 'left') {
				labelEl.classList.add('col-3');
			}
			if (labelPosition === 'top') {
				labelEl.classList.add('col-9');
			}
			this.el.appendChild(labelEl);
		}

		const inputEl = document.createElement('input');
		inputEl.setAttribute('id', id);
		inputEl.value = defaultValue;
		inputEl.setAttribute('placeholder', placeholder);
		inputEl.setAttribute('type', type);
		// inputEl.classList.add('form-control'); // 오류나면 복구

		switch (variant) {
			case 'background':
				inputEl.classList.add('input-background');
				break;
			default:
				// 기본은 bright
				inputEl.classList.add('input-bright');
		}``

		switch (size) {
			case 's':
				inputEl.classList.add('form-control');
				if (label !== 'none')
					labelEl.classList.add('small'); // Bootstrap의 작은 텍스트 클래스
				break;
			case 'l':
				inputEl.classList.add('form-control-lg');
				if (label !== 'none')
					labelEl.classList.add('fs-1'); // Bootstrap의 큰 텍스트 클래스
				break;
			case 'xl':
				inputEl.classList.add('form-control-xl');
				if (label !== 'none')
					labelEl.classList.add('fs-0')
		}

		if (labelPosition === 'top')
			inputEl.classList.add('col-12');
		else
			inputEl.classList.add('col-9');
		this.el.appendChild(inputEl);

		this.render();
	}

	getValue() {
		const value = this.el.querySelector('input').value.trim();
		let label = '';
		if (this.el.querySelector('label')) {
			label = this.el.querySelector('label').textContent;
		}

		if (!value) {
			if (label === '') {
				throw new Error('값을 입력해주세요.');
			}
			throw new Error(`${label}을(를) 입력해주세요.`);
		}
	
		// SQL Injection 및 XSS 방지: 특정 패턴 필터링
		const forbiddenPatterns = /[<>;'"`]/;
		if (forbiddenPatterns.test(value)) {
			throw new Error('/[<>;\'"`]/ 문자를 사용할 수 없습니다.');
		}
		return value;
	}

	setValue(value) {
		this.el.querySelector('input').value = value;
	}

	render() {
		// 추가적인 렌더링 로직이 필요할 경우 여기에 작성
	}
}