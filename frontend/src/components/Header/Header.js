import { Component, getCookie } from "../../core/core.js";
import { CharactorProfile } from "../Profile/profile.js";
import { MyProfileContent } from "../MyProfileContent/MyProfileContent.js";

export class Header extends Component {
    constructor(props) {
        super();
        this.props = props;
        this.headerRender(props);
    }
    headerRender(props) {
        this.el.classList.add('header');
        this.el.innerHTML = /*html*/`
            <button class="return">42 PP</button>
            <div class="profile"></div>
        `;
        const player = getCookie('player');
        const profile = new CharactorProfile(props.profile_img, player);
        this.el.querySelector('.profile').appendChild(profile.el);
        this.el.querySelector('.return').addEventListener('click', () => {
            location.href = '/#/';
        });
        
        // CharactorProfile 클릭 이벤트: SelectPage의 내용을 MyProfileContent로 변경
        this.el.querySelector('.charactor-profile').addEventListener('click', () => {
            const selectPagePos = document.querySelector('.selectpagepos'); // SelectPage 위치 찾기
            selectPagePos.innerHTML = ''; // 현재 SelectPage 내용을 지움
            const myProfileContent = new MyProfileContent(); // 새로운 MyProfileContent 생성
            selectPagePos.appendChild(myProfileContent.el); // 새로운 내용을 삽입
        });
    }
}
