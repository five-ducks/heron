import { Component } from "../../core/core.js";
import { Avatar } from "./Avatar.js";

export class FriendProfile extends Component {
    constructor(name = 'unknown', image = 0, status_msg = '', onSelect = () => { }) {
        super({
            tagName: 'button'
        });
        const img = new Avatar(image, 'm');
        this.el.appendChild(img.el);

        // 프로필 정보를 담을 div 생성
        const infoContainer = document.createElement('div');
        infoContainer.classList.add('info-container');
        this.el.appendChild(infoContainer);

        // 첫 번째 span: 닉네임
        const spanNick = document.createElement('span');
        spanNick.textContent = name;
        infoContainer.appendChild(spanNick);

        // 두 번째 span: 상태 메시지
        const spanAdditional = document.createElement('span');
        spanAdditional.textContent = status_msg;
        infoContainer.appendChild(spanAdditional);

        this.isSelected = false;
        this.el.addEventListener('click', onSelect);
        this.render();
    }

    render() {
        this.el.classList.add('charactor-profile');
    }
}
