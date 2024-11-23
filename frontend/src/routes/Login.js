import { Component } from "../core/core.js";
import { Button } from "../components/Button.js";
import { JoinModal } from "../components/JoinModal/JoinModal.js";
import { Input } from "../components/Input/Input.js";
import { getCookie } from "../core/core.js";
import { quickAlert } from "../components/Alert/Alert.js";

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
            await quickAlert('로그인 성공!', '확인');
            localStorage.setItem('currentView', 'selectPage');
            window.location.href = '#/main';
        } else if (response.status === 400) {
            await quickAlert('아이디 혹은 비밀번호가 일치하지 않습니다.', '확인');
        }
    } catch (error) {
        await quickAlert(`에러: ${error.message}`, '확인');
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
            await quickAlert(message.error, '확인');
        }
    } catch (error) {
        await quickAlert(`에러: ${error.message}`, '확인');
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
            <h1 class="login-title" style="font-family: var(--title-font);">login</h1>
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
                try {
                    const username = inputID.getValue(); // getValue() 사용
                    const password = inputPW.getValue(); // getValue() 사용
                    await loginUser(username, password);
                }
                catch (error) {
                    await quickAlert(`에러: ${error.message}`, '확인');
                }
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
