import { Component } from "../core/core.js";
import { Button } from "../components/Button.js";
import { JoinModal } from "../components/JoinModal/JoinModal.js";
import { Input } from "../components/Input/Input.js";
import { getCookie } from "../core/core.js";
import { CustomAlert } from "../components/Alert/Alert.js";

export default class Login extends Component {
    constructor() {
        super({
            props: {
                className: 'login',
            }
        });
    }
    render() {
        this.el.innerHTML = /*html*/`
        <h1>login</h1>
        <div class="login-input-container">
        </div>
        <div class="button-row"></div>
        `;

        // 쿠키를 저장하는 함수
        function setCookie(name, value, days) {
            const expires = new Date(Date.now() + days * 864e5).toUTCString();
            document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; domain=${window.location.hostname}; Secure; SameSite=Lax`;
        }

        // Initialize input fields
        const inputID = new Input({
            placeholder: 'Your nickname!',
            variant: 'background',
            id: 'nickname',
            label: 'ID',
        });
        const inputPW = new Input({
            placeholder: 'Password',
            variant: 'background',
            type: 'password',
            id: 'password',
            label: 'PW',
        });

        // Create buttons
        const loginButton = new Button({
            style: 'gray',
            size: 'm',
            text: 'Login'
        },
            async () => {
                // Retrieve input values
                const username = inputID.getValue(); // getValue() 사용
                const password = inputPW.getValue(); // getValue() 사용
                // Basic validation
                if (!username) {
                    const alert = new CustomAlert({
                        message: '아아디를 입력해주세요.',
                        okButtonText: '확인',
                    });
                    alert.render();
                    await alert.show();
                    return;
                }
                if (!password) {
                    const alert = new CustomAlert({
                        message: '비밀번호를 입력해주세요.',
                        okButtonText: '확인',
                    });
                    alert.render();
                    await alert.show();
                    return;
                }
                try {
                    // Send login request
                    const response = await fetch('/api/users/login/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            // back에게 request 내용 중 token도 보내줘야함(?)
                            'X-CSRF-Token': getCookie('csrftoken'),
                        },
                        body: JSON.stringify({ username, password }),
                    });
                    if (response.ok) {
                        const data = response;
                        setCookie('ppstate', data.status, 365);
                        sessionStorage.setItem('isLoggedIn', 'true');
                        setCookie('player', username, 365);
                        const alert = new CustomAlert({
                            message: '로그인 성공!',
                            okButtonText: '확인',
                        });
                        alert.render();
                        await alert.show();
                        window.location.href = '#/main'; // 로그인 성공 시 메인 페이지로 이동
                    } else {
                        const error = response;
                        const alert = new CustomAlert({
                            message: `-로그인 실패-\n${error.message || '알 수 없는 오류가 발생했습니다.'}`,
                            okButtonText: '확인',
                        });
                        alert.render();
                        await alert.show();
                    }
                } catch (error) {
                    const alert = new CustomAlert({
                        message: `Server error: ${error.message}`,
                        okButtonText: '확인',
                    });
                    alert.render();
                    await alert.show();
                }
            }
        );

        const authButton = new Button({
            style: 'gray',
            size: 'm',
            text: '42 Auth',
        },
            async () => {
                try {
                    const response = await fetch('/api/oauth/login/', {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRF-Token': getCookie('csrftoken'),
                        }
                    });

                    if (response.ok) {
                        const data = await response.json();
                        window.location.href = data.redirect_url;  // 리디렉션 처리
                    } else {
                        console.error('Login failed');
                    }
                } catch (error) {
                    console.error('Server error:', error);
                }
            }
        );

        const signUpButton = new Button({
            style: 'gray',
            size: 'm',
            text: 'JOIN',
        },
            () => {
                joinModal.open();
                document.body.append(joinModal.el);
            }
        );
        this.el.querySelector('.login-input-container').append(inputID.el);
        this.el.querySelector('.login-input-container').append(inputPW.el);
        this.el.querySelector('.button-row').append(loginButton.el, authButton.el, signUpButton.el);

        // Initialize Join Modal
        const joinModal = new JoinModal(() => {
            // Handle actions when the modal is closed
        });
    }
}
