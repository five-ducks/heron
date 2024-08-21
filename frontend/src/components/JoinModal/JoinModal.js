import { Modal } from "../../core/modal.js";
import { SelectCharactor } from "../SelectCharactor/SelectCharactor.js";
import { Button } from "../Button.js";

export class JoinModal extends Modal {
	constructor(onClose = () => {}) {
		const content = /*html*/`
			<h1>회원가입</h1>
			<div class="input_row">
				<div class="">
					<p class="label">닉네임</p>
					<input type="text" placeholder="7자 미만으로 입력해주세요">
				</div>
				<div>
					<p class="label">비밀번호</p>
					<input type="password" placeholder="비밀번호는 6자 이상이여야 합니다.">
				</div>
				<div>
					<p class="label">비밀번호 확인</p>
					<input type="password" placeholder="한 번 더 입력해주세요">
				</div>
			</div>
			<div class="charactor-row">
			</div>
		`;
		super(content, onClose);
		this.addCharactors();
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
