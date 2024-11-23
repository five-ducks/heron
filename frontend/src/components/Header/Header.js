import { Component } from "../../core/core.js";
import { Profile } from "../Profile/Profile.js";
import store from "../../store/game.js";


export class Header extends Component {
    constructor(props, switchViewCallback) {
        super({
            props: {
                className: 'header',
            }
        });
        this.props = props;
        this.switchViewCallback = switchViewCallback;
        this.headerRender(props);
    }

    headerRender(props) {
        this.el.innerHTML = /*html*/`
            <div class="return"></div>
            <div class="profile"></div>
        `;
        const player = store.state.userInfo.username;
        const profile = new Profile(props.profile_img, player, 'l');
        this.el.querySelector('.profile').appendChild(profile.el);

        this.el.querySelector('.return').addEventListener('click', () => {
            location.href = '/#/';
        });

        // Profile 클릭 이벤트: MyProfileContent로 전환
        this.el.querySelector('.profile').addEventListener('click', () => {
            this.switchViewCallback();
        });
    }
}