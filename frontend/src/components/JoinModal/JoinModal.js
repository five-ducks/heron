import { Modal } from "../Modal/index.js";
import { SelectCharactor } from "../SelectCharactor/SelectCharactor.js";
import { Button } from "../Button.js";
import { Input } from "../../components/Input/Input.js";
import { CustomAlert } from "../Alert/Alert.js";

export class JoinModal extends Modal {
    constructor(onClose = () => { }) {
        const content = /*html*/`
                <div class="input_join">
                </div>
                <div class="charactor-row">
                </div>
        `;
        super('회원 가입', content, onClose);
        this.addCharactors();

        const nameInput = new Input({
            placeholder: '7자 미만으로 입력해주세요',
            variant: 'background',
            label: '닉네임',
            type: 'text',
            size: 'm',
        });
        const pwInput = new Input({
            placeholder: '비밀번호는 6자 이상이여야 합니다.',
            variant: 'background',
            label: '비밀번호',
            type: 'password',
            size: 'm',
        });
        const curpwInput = new Input({
            placeholder: '한 번 더 입력해주세요',
            variant: 'background',
            label: '비밀번호 확인',
            type: 'password',
            size: 'm',
        });

        this.el.querySelector('.input_join').appendChild(nameInput.el);
        this.el.querySelector('.input_join').appendChild(pwInput.el);
        this.el.querySelector('.input_join').appendChild(curpwInput.el);

        // 완료 버튼 추가
        const finishButton = new Button({
            style: 'gray',
            size: 'xl',
            text: '완료',
        },
            async () => {
                // Validate inputs
                const username = nameInput.getValue();
                const password = pwInput.getValue();
                const confirmPassword = curpwInput.getValue();

            // Basic validation checks
            if (!username || username.length >= 7) {
                const alert = new CustomAlert({
                    message: '닉네임을 7자 미만으로 입력해주세요.',
                    okButtonText: '확인',
                });
                alert.render();
                await alert.show();
                return;
            }
            if (!password || password.length < 6) {
                const alert = new CustomAlert({
                    message: '비밀번호는 6자 이상이여야 합니다.',
                    okButtonText: '확인',
                });
                alert.render();
                await alert.show();
                return;
            }
            if (password !== confirmPassword) {
                const alert = new CustomAlert({
                    message: '비밀번호가 일치하지 않습니다.',
                    okButtonText: '확인',
                });
                alert.render();
                await alert.show();
                return;
            }

            // 요청 데이터 생성
            const requestData = {
                username,
                password,
                profile_img: this.selectedCharactorIndex, // 선택된 캐릭터 인덱스 포함
            };
            nameInput.setValue('');
            pwInput.setValue('');
            curpwInput.setValue('');
            try {
                // 요청 전송
                const response = await fetch('/api/users/join/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestData),
                });
                // 응답 처리
                if (response.status === 201) {
                    const alert = new CustomAlert({
                        message: '회원가입이 완료되었습니다!',
                        okButtonText: '확인',
                    });
                    alert.render();
                    await alert.show();
                    this.close();  // 모달 닫기
                } else if (response.status === 400) {
                    const responseData = await response.json();
                    const error = responseData.error;  // 오류 메시지 가져오기
                    const alert = new CustomAlert({
                        message: `에러: ${response.status}, ${error}`,
                        okButtonText: '확인',
                    });
                    alert.render();
                    await alert.show();
                } else {
                    const alert = new CustomAlert({
                        message: '알 수 없는 오류가 발생했습니다.',
                        okButtonText: '확인',
                    });
                    alert.render();
                    await alert.show();
                }
            } catch (error) {
                const alert = new CustomAlert({
                    message: `서버 오류: ${error.message}`,
                    okButtonText: '확인',
                });
                alert.render();
                await alert.show();
            }
        });

        finishButton.el.classList.add('finish-button');
        this.el.querySelector('.modal-body').append(finishButton.el);
    }

    addCharactors() {
        const charactorRow = this.el.querySelector('.charactor-row');
        const charactors = new SelectCharactor();
        charactorRow.appendChild(charactors.el);

        // 캐릭터 선택 이벤트 리스너 추가 (default: 0)
        this.selectedCharactorIndex = 0; // 캐릭터 인덱스 기본값 설정
        charactors.el.addEventListener('charactorSelected', (event) => {
            this.selectedCharactorIndex = event.detail.index; // 선택된 캐릭터 인덱스 저장
        });
    }

}
