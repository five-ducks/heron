import { Component } from "../../core/core.js";
import { FriendProfile } from "../Profile/FriendProfile.js";

export class Sidebar extends Component {
    render() {
        this.el.classList.add('friendwindow');
        this.el.innerHTML = /*html*/`
            <button class="addfriend">친구추가 +</button>
            <div class="friends">
            </div>
        `;

        const friend = new FriendProfile('taehkim2', "../public/images/charactors/bulbasaur.png");
        const friend1 = new FriendProfile('minkylee', "../public/images/charactors/mew.png");
        const friend2 = new FriendProfile('sihlee', "../public/images/charactors/ditto.png");
        const friend3 = new FriendProfile('kangmlee', "../public/images/charactors/snorlax.png");
        friend.el.classList.add('friend');
        this.el.querySelector('.friends').appendChild(friend.el);
        this.el.querySelector('.friends').appendChild(friend1.el);
        this.el.querySelector('.friends').appendChild(friend2.el);
        this.el.querySelector('.friends').appendChild(friend3.el);
    }
}
