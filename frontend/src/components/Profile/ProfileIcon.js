import { Component } from "../../core/core.js";

export class ProfileIcon extends Component {
    constructor ( imageIndex = 0 ) {
        super(
            {
                tagName: 'img',
                classNames: ['profile-icon']
            }
        );
        const images = [
            "../public/images/charactors/pikachu.png",
            "../public/images/charactors/bulbasaur.png",
            "../public/images/charactors/charmander.png",
            "../public/images/charactors/ditto.png",
            "../public/images/charactors/eevee.png",
            "../public/images/charactors/mew.png",
            "../public/images/charactors/snorlax.png",
            "../public/images/charactors/squirtle.png"
        ];
        const src = images[imageIndex];
        this.el.src = src;
        // frame div 추가
        const frame = document.createElement('div');
        frame.classList.add('icon_frame');
        this.el.append(frame);
    }
    render() {
    }
}
