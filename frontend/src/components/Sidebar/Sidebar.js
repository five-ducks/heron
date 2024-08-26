import { Component } from "../../core/core.js";
import { FriendProfile } from "../Profile/FriendProfile.js";
import { InfoFriendModal } from "../InfoFriendModal/InfoFriendModal.js";

export class Sidebar extends Component {
    render() {
        this.el.classList.add('friendwindow');
        this.el.innerHTML = /*html*/`
            <button class="addfriend">친구추가 +</button>
            <div class="friends"></div>
        `;

        const info_f1 = new InfoFriendModal(() => console.log('info_f1'));
        document.body.appendChild(info_f1.el);  // 아 없는데 어떻게 띄워!!!!!
        const friend = new FriendProfile('taehkim2', "../public/images/charactors/bulbasaur.png", () => {
            info_f1.open();
			console.log('info open');
        });
        const friend1 = new FriendProfile('minkylee', "../public/images/charactors/mew.png");
        const friend2 = new FriendProfile('sihlee', "../public/images/charactors/ditto.png");
        const friend3 = new FriendProfile('kangmlee', "../public/images/charactors/snorlax.png");

        this.el.querySelector('.friends').appendChild(friend.el);
        this.el.querySelector('.friends').appendChild(friend1.el);
        this.el.querySelector('.friends').appendChild(friend2.el);
        this.el.querySelector('.friends').appendChild(friend3.el);
    }
}
