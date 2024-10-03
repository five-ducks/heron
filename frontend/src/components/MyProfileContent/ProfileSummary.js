import { Component, getCookie, selectProfileImg } from "../../core/core.js";
import { ProfileLevel } from "./ProfileLevel.js";
import { Button } from "../Button.js";
import { Input } from "../Input.js";

export class ProfileSummary extends Component {
	constructor(props) {
		super({
			props: {
				className: 'profile-summary',
			}
		});
		this.profileContentsRender(props);
	}

	profileContentsRender(props) {
		const username = getCookie('player');
		this.el.innerHTML = /*html*/`
			<div class="profile-summary-img-level">
				<div class="profile-summary-img"></div>
			</div>
			<div class="profile-summary-name">
				<div>${username}</div>
			</div>
			<div class="vertical-line"></div>
			<div class="profile-summary-win">
				<p>승부 요약</p>
				<span>${props.win_cnt}승 ${props.lose_cnt}패</span>
			</div>
			<div class="vertical-line"></div>
			<div class="button-container"></div>
		`;

		//프로필 이미지
		const profileImg = this.el.querySelector('.profile-summary-img');
		const img = document.createElement('img');
		img.src = selectProfileImg(props.profile_img);
		profileImg.appendChild(img);

		//유저 이름 & 프로필 레벨
		const profileImgLevel = this.el.querySelector('.profile-summary-img-level');
		profileImgLevel.appendChild(new ProfileLevel(props.exp).el);

		const profileName = this.el.querySelector('.profile-summary-name');

		profileName.appendChild(new Input(
			'', 'text', {
			background: "url('../../../public/images/ui/profile-input.png')",
			width: '300px',
			height: '50px',
			fontsize: '20px',
		}, props.status_msg).el);

		// 승부 요약
		const profileWin = this.el.querySelector('.profile-summary-win');

		const logoutBtn = new Button({
			width: '130px',
			height: '60px',
			size: '25px',
			background: "url('../../../public/images/ui/profile-button.png')",
		},
			'로그아웃',
			async () => {
				const response = await fetch('/api/users/logout', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRF-Token': getCookie('csrftoken'),
					},
				});
				const status = response.status;
				if (status === 200) {
					document.cookie = 'ppstate=; player=;';
					location.href = '/#/';
					alert('로그아웃 되었습니다.');
				}
				else
					alert('로그아웃에 실패했습니다.');
			}
		);
		const withdrawalBtn = new Button({
			width: '130px',
			height: '60px',
			size: '25px',
			background: "url('../../../public/images/ui/profile-button.png')",
		},
			'회원탈퇴',
			async () => {
				if (!confirm('정말로 탈퇴하시겠습니까?'))
					return;
				const response = await fetch('/api/users/self', {
					method: 'DELETE',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRF-Token': getCookie('csrftoken'),
					},
				});
				const status = response.status;
				if (status === 200) {
					document.cookie = 'ppstate=; player=;';
					location.href = '/#/';
					alert('회원탈퇴 되었습니다.');
				}
				else
					alert('회원탈퇴에 실패했습니다.');
			});

		const saveBtn = new Button({
			width: '200px',
			height: '100px',
			size: '25px',
			background: "url('../../../public/images/ui/profile-button.png')",
		},
			'저장하기',
			async () => {
				const request_body = {};
				const add_field = (selector, key, scope = this.el) => { // element에 접근하여 key에 해당하는 value를 request_body에 추가
					const inputElement = scope.querySelector(selector); // Get the input element within the specified scope
					if (inputElement) {
						const value = inputElement.value.trim(); // 양 끝 공백 제거
						if (value) {
							request_body[key] = value;
						}
					}
				};

				// 현재 입력된 값을 request_body에 추가
				add_field('.profile-summary-name input', 'status_msg');
				const parentBlock = this.el.closest('.my-profile-content');
				const macroBlock = parentBlock.querySelector('.my-macro');
				for (let i = 1; i <= 5; i++) {
					add_field(`.macro-input.f${i} input`, `macrotext${i}`, macroBlock);
				}

				// props와 request_body를 비교하여 달라진 내용만 request_body에 남기기
				if (props.status_msg === request_body.status_msg) {
					delete request_body.status_msg;
				}
				for (let i = 1; i <= 5; i++) {
					if (props.macrotext[i-1] === request_body[`macrotext${i}`]) {
						delete request_body[`macrotext${i}`];
					}
				}

				if (Object.keys(request_body).length === 0) {
					alert('변경된 내용이 없습니다.');
					return;
				}

				const response = await fetch('/api/users/self', {
					method: 'PATCH',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRF-Token': getCookie('csrftoken'),
					},
					body: JSON.stringify(request_body),
				});
				const status = response.status;
				if (status === 200) {
					alert('저장되었습니다.');
					location.reload();
				}
				else
					alert('저장에 실패했습니다.');
			});
		this.el.querySelector('.button-container').appendChild(logoutBtn.el);
		this.el.querySelector('.button-container').appendChild(withdrawalBtn.el);
		this.el.appendChild(saveBtn.el);
	}
}