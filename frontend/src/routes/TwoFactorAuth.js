import { Component, getCookie } from "../core/core.js";
import { Input } from "../components/Input/Input.js";
import { Button } from "../components/Button.js";
import { CustomAlert } from "../components/Alert/Alert.js";

export default class TwoFactorAuth extends Component {
    constructor() {
        super({
            props: {
                // className: 'two-factor-auth container row justify-content-center align-items-center',
                className: 'two-factor-auth container flex-column align-items-center',
            }
        });

        this.state = {
            isRequestSent: false,
            qrData: null // QR 데이터를 공유 상태로 관리
        };
    }

    async request2FA() {
        try {
            const hash = window.location.hash;
            const queryString = hash.split('?')[1];
            const urlParams = new URLSearchParams(queryString);
            const username = urlParams.get('username');

            const response = await fetch(`/api/auth/2fa/generate/?username=${username}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': getCookie('csrftoken'),
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || '2FA 요청 실패');
            }

            const data = await response.json();
            this.state.qrData = data.qr_code; // QR 코드 데이터를 상태에 저장
            this.state.isRequestSent = true;
            this.render();
        } catch (error) {
            console.error('2FA Request Error:', error);
            await this.showAlert(`오류: ${error.message}`);
        }
    }

    async generateQRCode() {
        try {
            if (!this.state.qrData) {
                throw new Error('QR 데이터가 없습니다.');
            }

            const binary = atob(this.state.qrData);
            const bytes = Uint8Array.from(binary, char => char.charCodeAt(0));
            const qrBlob = new Blob([bytes], { type: 'image/png' });
            const qrUrl = URL.createObjectURL(qrBlob);

            const qrCanvas = document.createElement('canvas');
            const qrImage = new Image();
            qrImage.src = qrUrl;

            await new Promise((resolve, reject) => {
                qrImage.onload = () => {
                    qrCanvas.width = qrImage.width;
                    qrCanvas.height = qrImage.height;
                    qrCanvas.getContext('2d').drawImage(qrImage, 0, 0);
                    resolve();
                };
                qrImage.onerror = () => reject(new Error('QR 이미지 로드 실패'));
            });

            return qrCanvas;
        } catch (error) {
            console.error('QR Code generation error:', error);
            throw new Error('QR 코드 생성 실패');
        }
    }

    async verify2FA(code) {
        try {
            const hash = window.location.hash;

            // ? 뒤의 쿼리 문자열 부분을 추출합니다.
            const queryString = hash.split('?')[1];

            // URLSearchParams를 사용하여 쿼리 문자열을 파싱합니다.
            const urlParams = new URLSearchParams(queryString);

            // 'username' 파라미터의 값을 추출합니다.
            const username = urlParams.get('username');

            console.log(username);
            const response = await fetch(`/api/auth/2fa/verify/?username=${username}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': getCookie('csrftoken'),
                },
                body: JSON.stringify({ code: code }),
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || '2FA 인증 실패. 코드를 다시 확인해주세요.');
            }

            await this.showAlert('2FA 인증 성공!');
            window.location.href = '#/main';
        } catch (error) {
            console.error('2FA Verification Error:', error);
            await this.showAlert(`오류: ${error.message}`);
        }
    }

    async showAlert(message) {
        const alert = new CustomAlert({
            message,
            okButtonText: '확인',
        });
        alert.render();
        await alert.show();
    }

    renderQRCode() {
        const qrContainer = this.el.querySelector('.qr-image-container');
        if (qrContainer) {
            if (this.state.qrData) {
                this.generateQRCode()
                    .then(qrCanvas => {
                        qrContainer.innerHTML = '';
                        qrContainer.appendChild(qrCanvas);
                    })
                    .catch(error => console.error('QR Code rendering error:', error));
            } else {
                qrContainer.innerHTML = `<p>QR 데이터를 로드 중입니다...</p>`;
            }
        }
    }

    render() {
        this.el.innerHTML = /*html*/`
                <h1 style="font-family: var(--title-font);">2-Factor Authentication</h1>
                <div class="qr-image-container"></div>
                ${!this.state.isRequestSent
                ? `<button class="btn btn-primary" id="generateQR">QR 코드 생성</button>`
                : `<p>QR 코드를 인증 앱으로 스캔해주세요</p>`}
                <div class="two-factor-input-container d-flex flex-row gap-3"></div>
        `;

        if (!this.state.isRequestSent) {
            this.request2FA()
        } else {
            const inputContainer = this.el.querySelector('.two-factor-input-container');

            const codeInput = new Input({
                placeholder: 'Enter verification code',
                variant: 'background',
                id: '2fa-code',
                size: 'l',
            });

            const verifyButton = new Button({
                style: 'gray',
                size: 'xl',
                text: 'Verify',
            }, async () => {
                const code = codeInput.getValue();
                if (!code) {
                    await this.showAlert('인증 코드를 입력해주세요.');
                    return;
                }
                await this.verify2FA(code);
            });

            inputContainer.append(codeInput.el);
            codeInput.el.classList.add('col-9');
            inputContainer.append(verifyButton.el);
        }

        this.renderQRCode();
    }
}
