import { Component } from "../../core/core.js";
import { Avatar } from "./Avatar.js";

export class Profile extends Component {
    constructor(image = 0, name = "unknown", size = 'm', options = {}) {
        super({
            tagName: 'button'
        });
        
        const { status_msg, onSelect = () => {} } = options;
        
        this.size = size;
        this.el.classList.add(`size-${this.size}`);
        
        // Avatar 생성
        const img = new Avatar(image, size);
        this.el.appendChild(img.el);

        // 정보를 담을 컨테이너 생성
        const infoContainer = document.createElement('div');
        infoContainer.classList.add('info-container');
        this.el.appendChild(infoContainer);

        // 이름 span 생성
        const nameSpan = document.createElement('span');
        nameSpan.textContent = name;
        nameSpan.classList.add('character-name');
        infoContainer.appendChild(nameSpan);

        // status_msg가 제공된 경우에만 추가 span 생성
        if (status_msg) {
            const statusSpan = document.createElement('span');
            statusSpan.textContent = status_msg;
            statusSpan.classList.add('status-message');
            infoContainer.appendChild(statusSpan);
        }

        this.isSelected = false;
        this.el.addEventListener('click', () => { onSelect(this); });

        this.render();
    }

    render() {
        this.el.classList.add('character-profile', `size-${this.size}`);
    }
}