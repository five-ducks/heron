import { Component } from "../../core/core.js";
import { CharactorProfile } from "../Profile/profile.js";

export class Header extends Component {
    render() {
        this.el.classList.add('header');
        this.el.innerHTML = /*html*/`
            <button class="return">42 PP</button>
            <div class="space"></div>
            <div class="profile"></div>
        `;
        const profile = new CharactorProfile();
        this.el.querySelector('.profile').appendChild(profile.el);
    }
}
