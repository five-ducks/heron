import { Component, getCookie } from "../core/core.js";
import { Input } from "../components/Input/Input.js";
import { Button } from "../components/Button.js";
import { CustomAlert } from "../components/Alert/Alert.js";

export default class TwoFactorAuth extends Component {
    constructor() {
        super({
            props: {
                className: 'two-factor-auth container row justify-content-center align-items-center',
            }
        });

        this.state = {
            isRequestSent: false,
            qrData: null
        };
    }

    async request2FA() {
        try {
            const resUri = localStorage.getItem('username');
            const response = await fetch(`/api/auth/2fa/generate/?username=${resUri}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': getCookie('csrftoken'),
                    'username': localStorage.getItem('username'),
                }

            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || '2FA 요청 실패');
            }


            // const data = await response.json();
            // 백엔드에서 받은 데이터로 QR 코드 생성
            // const qrCanvas = await this.generateQRCode(data.qrData);

            this.state.isRequestSent = true;
            // this.state.qrData = data.qrData;
            // this.render();

            // QR 코드 캔버스를 DOM에 추가
            // const qrContainer = this.el.querySelector('.qr-image-container');
            // if (qrContainer) {
            //     qrContainer.innerHTML = '';
            //     qrContainer.appendChild(qrCanvas);
            // }

            // await this.showAlert('QR 코드가 생성되었습니다. 인증 앱으로 스캔해주세요.');
            console.log(response);
            await console.log(response.json());
            console.log(response.json().Object);

            const bytes = new Uint8Array(response.json().data);
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
                qrImage.onerror = reject;
            });

        } catch (error) {
            console.error('2FA Request Error:', error);
            await this.showAlert(`오류: ${error.message}`);
        }
    }

    async verify2FA(code) {
        try {
            const response = await fetch('/api/auth/verify-2fa/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': getCookie('csrftoken'),
                },
                body: JSON.stringify({ code }),
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

    render() {
        this.el.innerHTML = /*html*/`
            <div class="two-factor-container d-flex flex-column align-items-center gap-4">
                <h1 class="two-factor-title" style="font-family: var(--title-font);">2-Factor Authentication</h1>
                <div class="qr-container text-center mb-4">
                    <div class="qr-image-container mb-3"></div>
                    ${!this.state.isRequestSent ?
                `<button class="btn btn-primary" id="generateQR">QR 코드 생성</button>` :
                `<p class="text-muted">QR 코드를 인증 앱으로 스캔해주세요</p>`
            }
                </div>
                <div class="two-factor-input-container"></div>
                <div class="button-row d-flex justify-content-center gap-3"></div>
            </div>
        `;

        // QR 코드 생성 버튼 이벤트 리스너
        if (!this.state.isRequestSent) {
            const generateButton = this.el.querySelector('#generateQR');
            if (generateButton) {
                generateButton.addEventListener('click', () => this.request2FA());
            }
        } else {
            const inputContainer = this.el.querySelector('.two-factor-input-container');
            const buttonRow = this.el.querySelector('.button-row');

            // 인증 코드 입력 단계
            const codeInput = new Input({
                placeholder: 'Enter verification code',
                variant: 'background',
                id: '2fa-code',
                label: 'Code',
                labelPosition: 'left',
                size: 'xl',
            });

            const verifyButton = new Button({
                style: 'gray',
                size: 'xxl',
                text: 'Verify'
            }, async () => {
                const code = codeInput.getValue();
                if (!code) {
                    await this.showAlert('인증 코드를 입력해주세요.');
                    return;
                }
                await this.verify2FA(code);
            });

            const resendButton = new Button({
                style: 'outline',
                size: 'xxl',
                text: 'Regenerate QR'
            }, async () => {
                await this.request2FA();
            });

            inputContainer.append(codeInput.el);
            buttonRow.append(verifyButton.el, resendButton.el);
        }



        // 이미 QR 데이터가 있다면 QR 코드 다시 생성
        if (this.state.qrData) {
            this.generateQRCode(this.state.qrData)
                .then(qrCanvas => {
                    const qrContainer = this.el.querySelector('.qr-image-container');
                    if (qrContainer) {
                        qrContainer.innerHTML = '';
                        qrContainer.appendChild(qrCanvas);
                    }
                })
                .catch(error => console.error('QR Code regeneration error:', error));
        }
    }
}