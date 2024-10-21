import { Component, getCookie } from "../../core/core.js";
import { MyProfileContent } from "../MyProfileContent/MyProfileContent.js";
import { Profile } from "../Profile/Profile.js";

export class Header extends Component {
    constructor(props) {
        super({
                props: {
                    className: 'header',
                }
            });
        this.props = props;
        this.headerRender(props);
    }
    headerRender(props) {
        this.el.innerHTML = /*html*/`
            <div class="return"></div>
            <div class="profile"></div>
        `;
        const player = getCookie('player');
        const profile = new Profile(props.profile_img, player, 'l');
        this.el.querySelector('.profile').appendChild(profile.el);
        this.el.querySelector('.return').addEventListener('click', () => {
            location.href = '/#/';
        });
        
        // CharactorProfile 클릭 이벤트: SelectPage의 내용을 MyProfileContent로 변경
        this.el.querySelector('.profile').addEventListener('click', () => {
            const gameSection = document.querySelector('.game-section'); // SelectPage 위치 찾기
            gameSection.innerHTML = ''; // 현재 SelectPage 내용을 지움
            const myProfileContent = new MyProfileContent(); // 새로운 MyProfileContent 생성
            gameSection.appendChild(myProfileContent.el); // 새로운 내용을 삽입
        });
    }
}
