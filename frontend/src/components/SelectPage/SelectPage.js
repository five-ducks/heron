import { Component } from "../../core/core.js";

export class SelectPage extends Component {
    render() {
        this.el.classList.add('selectpage');
        this.el.innerHTML = /*html*/`
            <div class="contents">
                <div class="title">게임 선택</div>
                <div class="game-list">
                    <button class="game1">1 : 1</button>
                    <button class="game2">토너먼트</button>
                </div>
            </div>
        `;

        // Add event listener to the game1 button
        const game1Button = this.el.querySelector('.game1');
        game1Button.addEventListener('click', () => {
            // Update the hash and load the temp.html page
            window.location.hash = '/game/onetoone/1';
            window.location.href = 'temp.html';
        });
    }
}