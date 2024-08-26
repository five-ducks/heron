import { Modal } from "../../core/modal.js";
import { SelectCharactor } from "../SelectCharactor/SelectCharactor.js";
import { Button } from "../Button.js";
import { Input } from "../Input.js";

export class JoinModal extends Modal {
	constructor(onClose = () => {}) {
		const content = /*html*/`
			<h1>회원가입</h1>
			<div class="join_row">
				<div class="input_join">
					<p class="joinInputLabel">닉네임</p>
					<div id="nickInput"></div>
				</div>
				<div class="input_join">
					<p class="joinInputLabel">비밀번호</p>
					<div id="pwInput"></div>
				</div>
				<div class="input_join">
					<p class="joinInputLabel">비밀번호 확인</p>
					<div id="curpwInput"></div>
				</div>
			</div>
			<div class="charactor-row">
			</div>
		`;
		super(content, onClose);
		this.addCharactors();
		const nickInput = new Input('7자 미만으로 입력해주세요', 'text', { width: '333px', height: '30px', fontsize: '20px'});
		const pwInput = new Input('비밀번호는 6자 이상이여야 합니다.', 'password', { width: '333px', height: '30px', fontsize: '20px' });
		const curpwInput = new Input('한 번 더 입력해주세요', 'password', { width: '333px', height: '30px', fontsize: '20px' });

		this.el.querySelector('#nickInput').appendChild(nickInput.el);
		this.el.querySelector('#pwInput').appendChild(pwInput.el);
		this.el.querySelector('#curpwInput').appendChild(curpwInput.el);

		const finishButton = new Button({ background: "url('../public/images/button.png')", width: '100px', height: '50px', size: '30px' }, '완료', () => {
			this.close();
			// 모달창 닫힐 때 처리할 내용
			// 유효성 검사 필요
		});
		finishButton.el.classList.add('finish-button');
		this.el.appendChild(finishButton.el);
	}

	addCharactors() {
		const charactorRow = this.el.querySelector('.charactor-row');
		const charactors = new SelectCharactor();
		charactorRow.appendChild(charactors.el);
		console.log(charactors.el);
	}
}
