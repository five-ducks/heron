import { Component } from "../core/core.js";
import { Button } from "../components/Button.js";
import { JoinModal } from "../components/JoinModal/JoinModal.js";
import { Input } from "../components/Input/Input.js";
import { getCookie } from "../core/core.js";
import { CustomAlert } from "../components/Alert/Alert.js";

// New function for login API request
async function loginUser(username, password) {
    try {
        const response = await fetch('/api/users/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': getCookie('csrftoken'),
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            const alert = new CustomAlert({
                message: '로그인 성공!',
                okButtonText: '확인',
            });
            alert.render();
            await alert.show();
            window.location.href = '#/main';
        } else {
            const message = await response.json();
            const alert = new CustomAlert({
                message: message.error,
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

// New function for 42 authentication API request
async function authenticate42() {
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
            window.location.href = data.redirect_url;
        } else {
            const message = await response.json();
            const alert = new CustomAlert({
                message: message.error,
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

export default class Login extends Component {
    constructor() {
        super({
            props: {
                className: 'login container row justify-content-center align-items-center', // Bootstrap container 클래스 추가
            }
        });
    }
    render() {
        this.el.innerHTML = /*html*/`
            <h1 class="login-title">login</h1>
            <div class="login-input-container"></div>
            <div class="button-row d-flex justify-content-center gap-3"></div>
        `;

        // Initialize input fields
        const inputID = new Input({
            placeholder: 'Your nickname!',
            variant: 'background',
            id: 'nickname',
            label: 'ID',
            labelPosition: 'left',
			size: 'xl',
        });
        const inputPW = new Input({
            placeholder: 'Password',
            variant: 'background',
            type: 'password',
            id: 'password',
            label: 'PW',
            labelPosition: 'left',
			size: 'xl',
        });

        // Create buttons
        const loginButton = new Button({
            style: 'gray',
            size: 'xxl',
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
                await loginUser(username, password);
            }
        );

        const authButton = new Button({
            style: 'gray',
            size: 'xxl',
            text: '42 Auth',
        },
            async () => {
                await authenticate42();
            }
        );

        const signUpButton = new Button({
            style: 'gray',
            size: 'xxl',
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
