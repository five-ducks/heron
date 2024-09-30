import { Component } from "../../core/core.js";

export class SelectPage extends Component {
    render() {
        this.el.classList.add('selectpage');
        this.el.innerHTML = /*html*/`
            <div class="contents">
                <div class="title">게임 선택</div>
                <div class="game-list">
                    <button class="onetoone">1 : 1</button>
                    <button class="tournament">토너먼트</button>
                </div>
            </div>
        `;

		// 1:1 게임 버튼 event listener
        const onetooneButton = this.el.querySelector('.onetoone');
        onetooneButton.addEventListener('click', () => {
            window.location.hash = '/game/onetoone/';
        });
    }
}