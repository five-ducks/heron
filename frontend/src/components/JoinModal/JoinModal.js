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
                    <div id="nameInput"></div>
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

        // 인풋 필드 생성
        const nameInput = new Input('7자 미만으로 입력해주세요', 'text', { width: '333px', height: '30px', fontsize: '20px'});
        const pwInput = new Input('비밀번호는 6자 이상이여야 합니다.', 'password', { width: '333px', height: '30px', fontsize: '20px' });
        const curpwInput = new Input('한 번 더 입력해주세요', 'password', { width: '333px', height: '30px', fontsize: '20px' });

        // 인풋 필드 추가
        this.el.querySelector('#nameInput').appendChild(nameInput.el);
        this.el.querySelector('#pwInput').appendChild(pwInput.el);
        this.el.querySelector('#curpwInput').appendChild(curpwInput.el);

        // 완료 버튼 추가
        const finishButton = new Button({ background: "url('../public/images/button.png')", width: '100px', height: '50px', size: '30px' }, '완료', async () => {
            // Validate inputs
            const username = nameInput.getValue();
            const password = pwInput.getValue();
            const confirmPassword = curpwInput.getValue();

            // Basic validation checks
            if (!username || username.length >= 7) {
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

            // const profile_img = this.selectedCharactorIndex;

            // 요청 데이터 생성
            const requestData = {
                username,
                password,
                profile_img: this.selectedCharactorIndex, // 선택된 캐릭터 인덱스 포함
            };
            console.log('requestData:', requestData);

            try {
                // 요청 전송
                const response = await fetch('/api/users/join', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestData),
                });
                // 응답 처리
                if (response.status === 201) {
                    alert('회원가입이 완료되었습니다!');
                    this.close();  // 모달 닫기
                } else if (response.status === 400) {
                    const responseData = await response.json();
                    const error = responseData.error;  // 오류 메시지 가져오기
                    alert(`error: ${response.status}, ${error}`);
                } else {
                    alert('알 수 없는 오류가 발생했습니다.');
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
    
        // 캐릭터 선택 이벤트 리스너 추가
        charactors.el.addEventListener('charactorSelected', (event) => {
            this.selectedCharactorIndex = event.detail.index; // 선택된 캐릭터 인덱스 저장
        });
    }
    
}
