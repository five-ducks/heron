import { Component } from "../core/core.js";

export class Input extends Component {
	constructor(placeholder = 'Input', type = 'text', style = {}) {
		super({
			tagName: 'input'
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
			marginBottom = '0px'
		} = style;

		// 스타일 적용
		this.el.style.width = width;
		this.el.style.height = height;
		this.el.style.background = background; // 배경 색상과 이미지 조합
		this.el.style.backgroundSize = backgroundSize;
		this.el.style.backgroundPosition = backgroundPosition;
		this.el.style.fontFamily = fontfamily;
		this.el.style.fontSize = fontsize;
		this.el.style.marginBottom = marginBottom;

		// placeholder 및 type 설정
		this.el.setAttribute('placeholder', placeholder);
		this.el.setAttribute('type', type);

		this.render();
	}

	render() {
		// 추가적인 렌더링 로직이 필요할 경우 여기에 작성
	}
}
