import { Component, getCookie } from "../../core/core.js";
import { ProfileLevel } from "./ProfileLevel.js";
import { Button } from "../Button.js";
import { Input } from "../Input/Input.js";
import { quickAlert } from "../Alert/Alert.js";
import { closeWebSocketConnection } from "../../status/status.js";
import store from "../../store/game.js";
import { Avatar } from "../Avatar/Avatar.js";
import { stateValidationCheck } from "../../core/core.js";

export class ProfileSummary extends Component {
	constructor(props) {
		super({
			props: {
				className: 'profile-summary row',
			}
		});
		this.profileContentsRender(props);
	}

	profileContentsRender(props) {
		const username = store.state.userInfo.username;
		this.el.innerHTML = /*html*/`
			<div class="profile-summary-user-state col-6 row"></div>
			<div class="profile-summary-logandbtn col-6 row"></div>
		`;

		const profileStateArea = this.el.querySelector('.profile-summary-user-state');
		const profilebtnArea = this.el.querySelector('.profile-summary-logandbtn');
		const profileImg = new Avatar(
			props.profile_img,
			'm',
			props.status
		);

		//유저 이름 & 프로필 레벨
		const profileNameLevel = document.createElement('div');
		profileNameLevel.classList.add('col-2');
		profileNameLevel.appendChild(profileImg.el);
		profileNameLevel.appendChild(new ProfileLevel(props.level).el);
		profileStateArea.appendChild(profileNameLevel);

		const profileStateInput = new Input({
			label: `${username}의 기분`,
			variant: 'background',
			defaultValue: props.status_msg,
			size: 'l',
		});

		profileStateInput.el.classList.add('col-10', 'profile-state-input');
		profileStateArea.appendChild(profileStateInput.el);

		// 승부 요약
		// const profileWin = document.createElement('div');
		// profileWin.innerHTML = /*html*/`
		// 	<p>승부 요약</p>
		// 	<span>${props.win_cnt}승 ${props.lose_cnt}패</span>
		// `;
		// profileWin.classList.add('col-3', 'profile-win');
		// profilebtnArea.appendChild(profileWin);

		const logoutBtn = new Button({
			style: 'blue',
			size: 'sm',
			text: '로그아웃',
		},
			async () => {
				const response = await fetch('/api/auth/logout/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRF-Token': getCookie('csrftoken'),
					},
				});
				const status = response.status;
				if (status === 200) {
					closeWebSocketConnection();
					await quickAlert('로그아웃 되었습니다.');
					localStorage.removeItem('currentView');
					location.href = '/#/';
				}
				else {
					await quickAlert('로그아웃에 실패했습니다.');
				}
			}
		);

		const withdrawalBtn = new Button({
			style: 'blue',
			size: 'sm',
			text: '회원탈퇴',
		},
			async () => {
				if (!confirm('정말로 탈퇴하시겠습니까?'))
					return;
				const response = await fetch('/api/auth/self/', {
					method: 'DELETE',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRF-Token': getCookie('csrftoken'),
					},
				});
				const status = response.status;
				if (status === 200) {
					closeWebSocketConnection();
					await quickAlert('회원탈퇴 되었습니다.');
					location.href = '/#/';
				}
				else {
					await quickAlert('회원탈퇴에 실패했습니다.');
				}
			});

		const saveBtn = new Button({
			style: 'blue',
			size: 'sm',
			text: '저장하기',
		},
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
				add_field('.profile-summary-user-state input', 'status_msg');
				const parentBlock = this.el.closest('.my-profile-content');
				const macroBlock = parentBlock.querySelector('.my-macro');
				for (let i = 1; i <= 5; i++) {
					add_field(`#f${i}`, `macrotext${i}`, macroBlock);
				}

				// request_body의 유효성 검사
				try {
					for (let key in request_body) {
						console.log(key);
						console.log(request_body[key]);
						stateValidationCheck(request_body[key], key)
					}
				} catch (e) {
					await quickAlert(e);
					return;
				}

				// props와 request_body를 비교하여 달라진 내용만 request_body에 남기기
				if (props.status_msg === request_body.status_msg) {
					delete request_body.status_msg;
				}

				for (let i = 1; i <= 5; i++) {
					if (props.macrotext[i - 1] === request_body[`macrotext${i}`]) {
						delete request_body[`macrotext${i}`];
					}
				}

				const response = await fetch('/api/users/self/', {
					method: 'PATCH',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRF-Token': getCookie('csrftoken'),
					},
					body: JSON.stringify(request_body),
				});
				const status = response.status;
				if (status === 200) {
					await quickAlert('저장되었습니다.');
					location.reload();
				}
				else {
					await quickAlert('저장에 실패했습니다.');
				}
			});
		logoutBtn.el.classList.add('col-3', 'profile-logoutBtn');
		withdrawalBtn.el.classList.add('col-3', 'profile-withdrawalBtn');
		saveBtn.el.classList.add('col-3', 'profile-saveBtn');
		this.el.querySelector('.profile-summary-logandbtn').appendChild(logoutBtn.el);
		this.el.querySelector('.profile-summary-logandbtn').appendChild(withdrawalBtn.el);
		this.el.querySelector('.profile-summary-logandbtn').appendChild(saveBtn.el);
	}
}