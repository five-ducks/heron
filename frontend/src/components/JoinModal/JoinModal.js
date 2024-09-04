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

        // Initialize input fields
        const nickInput = new Input('7자 미만으로 입력해주세요', 'text', { width: '333px', height: '30px', fontsize: '20px'});
        const pwInput = new Input('비밀번호는 6자 이상이여야 합니다.', 'password', { width: '333px', height: '30px', fontsize: '20px' });
        const curpwInput = new Input('한 번 더 입력해주세요', 'password', { width: '333px', height: '30px', fontsize: '20px' });

        // Append input elements to the DOM
        this.el.querySelector('#nickInput').appendChild(nickInput.el);
        this.el.querySelector('#pwInput').appendChild(pwInput.el);
        this.el.querySelector('#curpwInput').appendChild(curpwInput.el);

        // Finish button with fetch logic
        const finishButton = new Button({ background: "url('../public/images/button.png')", width: '100px', height: '50px', size: '30px' }, '완료', async () => {
            // Validate inputs
            const nickname = nickInput.el.querySelector('input').value.trim();
            const password = pwInput.el.querySelector('input').value;
            const confirmPassword = curpwInput.el.querySelector('input').value;

            // Basic validation checks
            if (!nickname || nickname.length >= 7) {
                alert('닉네임을 7자 미만으로 입력해주세요.');
                return;
            }
            if (!password || password.length < 6) {
                alert('비밀번호는 6자 이상이여야 합니다.');
                return;
            }
            if (password !== confirmPassword) {
                alert('비밀번호가 일치하지 않습니다.');
                return;
            }

            // Prepare the registration data
            const requestData = {
                nickname,
                password,
                // Add more fields if necessary
            };

            try {
                // Send the fetch request
                const response = await fetch('api/user/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestData),
                });

                // Handle response
                if (response.ok) {
                    const data = await response.json();
                    alert('회원가입이 완료되었습니다!');
                    this.close();  // Close the modal on success
                } else {
                    const error = await response.json();
                    alert(`회원가입 실패: ${error.message || '알 수 없는 오류입니다.'}`);
                }
            } catch (error) {
                alert(`서버 오류: ${error.message}`);
            }
        });

        finishButton.el.classList.add('finish-button');
        this.el.appendChild(finishButton.el);
    }

    addCharactors() {
        const charactorRow = this.el.querySelector('.charactor-row');
        const charactors = new SelectCharactor();
        charactorRow.appendChild(charactors.el);
    }
}
