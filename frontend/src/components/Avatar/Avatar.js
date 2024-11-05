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
        
        this.el.classList.add(`Avatar--${size}`);
        const img = document.createElement('img');
        const src = selectProfileImg(imageIndex);
        img.src = src;
        img.classList.add('Avatar_img');
        this.el.appendChild(img);        
    }
    render() {
        this.el.classList.add('Avatar');
    }
}
