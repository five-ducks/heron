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

		// 1:1 게임 버튼 event listener
		// const onetooneButton = this.el.querySelector('.onetoone');
		// onetooneButton.addEventListener('click', () => {
		// 	// 게임 세션 생성 요청을 서버로 보냄
		// 	fetch('/api/game/create', { method: 'POST' })
		// 		.then(response => response.json())
		// 		.then(data => {
		// 			// 서버에서 받은 gameID로 경로를 이동
		// 			const gameID = data.gameID;
		// 			window.location.hash = `/game/onetoone/${gameID}`;
		// 		});
		// });

		// 1:1 게임 버튼 event listener
		// const onetooneButton = this.el.querySelector('.onetoone');
        // onetooneButton.addEventListener('click', async () => {
        //     try {
        //         // 백엔드에 게임 생성 요청
        //         const response = await fetch('/api/create-game', {
        //             method: 'POST',
        //             headers: {
        //                 'Content-Type': 'application/json'
        //             }
        //         });

        //         if (!response.ok) {
        //             throw new Error('게임 생성에 실패했습니다.');
        //         }

        //         const data = await response.json();
        //         const gameID = data.gameID;

        //         // 해시 라우트를 업데이트하여 게임 페이지로 이동
        //         window.location.hash = `#/game/onetoone/${gameID}`;
        //     } catch (error) {
        //         console.error('게임 생성 오류:', error);
        //         alert('게임을 생성하는 동안 오류가 발생했습니다.');
        //     }
        // });
    }
}