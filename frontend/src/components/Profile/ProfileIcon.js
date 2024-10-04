import { Component } from "../../core/core.js";
import { selectProfileImg } from "../../core/core.js";

export class ProfileIcon extends Component {
    constructor ( imageIndex = 0 ) {
        super(
            {
                tagName: 'img',
                classNames: ['profile-icon']
            }
        );
        const src = selectProfileImg(imageIndex);
        this.el.src = src;
        // frame div 추가
        const frame = document.createElement('div');
        frame.classList.add('icon_frame');
        this.el.append(frame);
    }
    render() {
    }
}
