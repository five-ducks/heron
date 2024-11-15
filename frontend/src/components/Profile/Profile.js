import { Component } from "../../core/core.js";
import { Avatar } from "../Avatar/Avatar.js";

export class Profile extends Component {
    constructor(image = 0, name = "unknown", size = 'm', options = {}) {
        const { status_msg, onSelect = () => {}, style, status } = options;
        
        super({
            tagName: 'button',
            props: {
                className: `character-profile size-${size}`,
            }
        });

        // Avatar 생성
        const img = new Avatar(image, size, status);
        
        if (style === "inner") {
            this.el.appendChild(img.el);
            const nameSpan = document.createElement('span');
            nameSpan.textContent = name;
            nameSpan.classList.add('inner-character-name');
            this.el.appendChild(nameSpan);
        } else {
            this.el.appendChild(img.el);
            this.createInfoContainer(name, status_msg);
            this.isSelected = false;
            this.el.addEventListener('click', () => { onSelect(this); });
        }
    }

    createInfoContainer(name, status_msg) {
        const infoContainer = document.createElement('div');
        infoContainer.classList.add('info-container');
        
        const nameSpan = document.createElement('span');
        nameSpan.textContent = name;
        nameSpan.classList.add('character-name');
        infoContainer.appendChild(nameSpan);

        if (status_msg) {
            const statusSpan = document.createElement('span');
            statusSpan.textContent = status_msg;
            statusSpan.classList.add('status-message');
            infoContainer.appendChild(statusSpan);
        }

        this.el.appendChild(infoContainer);
    }

    render() {
        // 렌더링 로직이 필요한 경우 여기에 추가
    }
}