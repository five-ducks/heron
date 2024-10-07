import { Component } from "../core/core.js";
import { Button } from "../components/Button.js";
import { JoinModal } from "../components/JoinModal/JoinModal.js";
import { Input } from "../components/Input.js";
import { getCookie } from "../core/core.js";

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
        const input_ID = new Input('Your Nickname!', 'text', {
            width: '440px',
            height: '80px'
        },
            '',
            'nickname',
            'nickname'
        );
        const input_PW = new Input('****', 'password', {
            width: '440px',
            height: '80px'
        }
            , '',
            'password',
            'password'
        );

        // Create buttons
        const loginButton = new Button(
            {
                background: "url('../public/images/button.png')",
                width: '300px',
                height: '169px',
                size: '70px'
            },
            'Login',
            async () => {
                // Retrieve input values
                const username = input_ID.getValue(); // getValue() 사용
                const password = input_PW.getValue(); // getValue() 사용

                // Basic validation
                if (!username) {
                    alert('Please enter your ID.');
                    return;
                }
                if (!password) {
                    alert('Please enter your password.');
                    return;
                }
                try {
                    // Send login request
                    const response = await fetch('/api/users/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            // back에게 request 내용 중 token도 보내줘야함(?)
                            'X-CSRF-Token': getCookie('csrftoken'),
                        },
                        body: JSON.stringify({ username, password }),
                    });
                    if (response.ok) {
                        const data = await response;
                        setCookie('ppstate', data.status, 365);
                        setCookie('player', username, 365);
                        alert('Login successful!');
                        window.location.href = '#/main'; // 로그인 성공 시 메인 페이지로 이동
                    } else {
                        const error = await response;
                        alert(`Login failed: ${error.message || 'Unknown error occurred.'}`);
                    }
                } catch (error) {
                    alert(`Server error: ${error.message}`);
                }
            }
        );

        const authButton = new Button(
            {
                background: "url('../public/images/button.png')",
                width: '300px',
                height: '169px',
                size: '70px',
            },
            '42 Auth',
            () => { }
        );

        const signUpButton = new Button(
            {
                background: "url('../public/images/button.png')",
                width: '300px',
                height: '169px',
                size: '70px',
            },
            'JOIN',
            () => {
                joinModal.open();
                this.el.appendChild(joinModal.el);
            }
        );
        this.el.querySelector('.login-input-container').append(input_ID.el);
        this.el.querySelector('.login-input-container').append(input_PW.el);
        this.el.querySelector('.button-row').append(loginButton.el, authButton.el, signUpButton.el);

        // Initialize Join Modal
        const joinModal = new JoinModal(() => {
            // Handle actions when the modal is closed
        });
    }


}
