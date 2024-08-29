import { Component } from "../core/core.js";
import { Button } from "../components/Button.js";
import { JoinModal } from "../components/JoinModal/JoinModal.js";
import { Input } from "../components/Input.js";

export default class Login extends Component {
    render() {
        this.el.innerHTML = /*html*/`
        <div class="login">
            <div class="container text-center">
                <div class="row">
                    <h1>login</h1>
                </div>
                <div class="inputLogin">
                    <div class="input_row" id="input_ID">
                        <div class="input_label"> ID </div>
                    </div>
                    <div class="input_row" id="input_PW">
                        <div class="input_label"> PW </div>
                    </div>
                </div>
                <div class="button-row">
                </div>
                <div class="button-row">
                </div>
            </div>
        </div>
        `;

        // Initialize input fields
        const input_ID = new Input('Your Nickname!', 'text', {
            width: '440px',
            height: '80px'
        });
        const input_PW = new Input('****', 'password', {
            width: '440px',
            height: '80px'
        });

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
				console.log(input_ID.getValue()); // debug
				console.log(input_PW.getValue()); // debug
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
                    const response = await fetch('/api/user/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ username, password }),
                    });

                    // Handle response
                    if (response.ok) {
                        const data = await response.json();
						console.log(data); // debug
                        alert('Login successful!');
                        // Perform actions after successful login (e.g., redirect, close modal, etc.)
                    } else {
                        const error = await response.json();
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
            () => { console.log('42 auth') }
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
                console.log('join')
            }
        );

        // Add input fields and buttons to the DOM
        input_ID.el.classList.add('input_field');
        input_PW.el.classList.add('input_field');
        this.el.querySelector('#input_ID').append(input_ID.el);
        this.el.querySelector('#input_PW').append(input_PW.el);
        this.el.querySelector('.button-row').append(loginButton.el, authButton.el, signUpButton.el);

        // Initialize Join Modal
        const joinModal = new JoinModal(() => {
            console.log('closed');
            // Handle actions when the modal is closed
        });
        this.el.appendChild(joinModal.el);
    }
}
