import { Component } from "../../core/core.js";
import { CharactorProfile } from "../Profile/profile.js";

export class Header extends Component {
    render() {
        this.el.classList.add('header');
        this.el.innerHTML = /*html*/`
            <button class="return">42 PP</button>
            <div class="profile"></div>
        `;
        const profile = new CharactorProfile();
        this.el.querySelector('.profile').appendChild(profile.el);
        this.el.querySelector('.return').addEventListener('click', () => {
            location.href = '/#/login';
        });
        this.el.querySelector('.charactor-profile').addEventListener('click', () => {
            location.href = '/#/myprofile';
        });
    }
}
