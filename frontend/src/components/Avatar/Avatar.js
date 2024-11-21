import { Component } from "../../core/core.js";
import { selectProfileImg } from "../../core/core.js";

export class Avatar extends Component {
    constructor ( imageIndex = 0, size = 'm', status = 0 ) {
        super({
            tagName: 'div',
            props: {
                className: 'Avatar'
            }
        });
        this.el.classList.add(`Avatar-${size}`);
        const img = document.createElement('img');
        const src = selectProfileImg(imageIndex);
        img.src = src;
        img.classList.add('Avatar-img');
        if (status === 0) {
            img.classList.add('Avatar-img-offline');
        } else if (status === 1) {
            img.classList.add('Avatar-img-online');
        }
        this.el.appendChild(img);
    }
    render() {
        this.el.classList.add('Avatar');
    }
}
