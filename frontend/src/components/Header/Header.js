import { Component, getCookie } from "../../core/core.js";
import { CharactorProfile } from "../Profile/profile.js";

export class Header extends Component {
    render() {
        this.el.classList.add('header');
        this.el.innerHTML = /*html*/`
            <button class="return">42 PP</button>
            <div class="profile"></div>
        `;
        const player = getCookie('player');
        const playerimages = 1;
        const profile = new CharactorProfile(playerimages, player);
        this.el.querySelector('.profile').appendChild(profile.el);
        this.el.querySelector('.return').addEventListener('click', () => {
            location.href = '/#/';
        });
        this.el.querySelector('.charactor-profile').addEventListener('click', () => {
            location.href = '/#/myprofile';
        });
    }
}
