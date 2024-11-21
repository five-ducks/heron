import { Component } from "../core/core.js";
import { handleServerMessage } from './messageHandler.js';
import { renderGame, draw, setPlayerNicknames, updateStatus } from './render.js';
import { handlePageLeave, handlePageReload } from './errorHandler.js'; 
import { getWebsocketUrl } from "./getWebsocket.js";
import { handleKeyPress } from './keyHandler.js';
import { initializeModal, initializeResultModal } from "./modal.js"

export class PingPongGame extends Component {
	constructor(payload = {}) {
        super(payload);
        this.socket = null;
        this.canvas = null;
        this.ctx = null;
		this.gameState = null;
		this.gameType = null;
        this.isGameStarted = false;
        this.playerSide = null;
		this.modalVisible = false;
		this.userInfo = null;

        // 뒤로가기 이벤트리스너
        window.addEventListener('popstate', () => handlePageLeave(this));

		// 새로고침 이벤트리스너
		// window.addEventListener('beforeunload', () => handlePageReload(this));

		// key 입력 이벤트리스너
		window.addEventListener('keydown', (e) => handleKeyPress(e, this));

        this.initializeWebSocket();
    }

    initializeWebSocket() {
        this.socket = new WebSocket(getWebsocketUrl(this));

		// socket 연결 성공
        this.socket.onopen = () => {
			updateStatus(this, 'Connected, waiting for opponent...');
        };
		// socket message 처리
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleServerMessage(this, data);
        };
		// socket 연결 종료
        this.socket.onclose = (event) => {
            if (event.wasClean) { // 정상정료시 true
                updateStatus(this, 'Closed cleanly');
            } else {
                updateStatus(this, 'Connection died');
            }
        };

		// socket 에러
        this.socket.onerror = (error) => {
            updateStatus(this, 'Error: ' + error.message);
        };
    }

	startOnetoonetGame(data) {
		this.gameState = data.state;
		this.playerSide = data.side;
		this.playerNumber = data.player;
        this.isGameStarted = true;

		this.render();
		setPlayerNicknames(this, data.player1Nickname, data.player2Nickname);

        const waitingScreen = this.el.querySelector('#waitingScreen');
        if (waitingScreen) {
            waitingScreen.style.display = 'none';
        } else {
            console.error("Waiting screen not found");
        }

        // canvas가 초기화되었는지 확인
        if (this.isCanvasInitialized && this.canvas) {
            this.canvas.style.display = 'block';
        } else {
            console.error("Canvas not found");
        }
        
        updateStatus(this, `Game Started! You are the ${this.playerSide} player.`);

        requestAnimationFrame(this.gameLoop.bind(this));
    }

    gameLoop() {
        if (!this.isGameStarted) {
			return;
		}

        draw(this);
        requestAnimationFrame(this.gameLoop.bind(this));
    }

    // 컴포넌트가 제거될 때 호출되는 메서드
    destroy() {
		// socket 연결 종료
		if (this.socket && this.socket.readyState === WebSocket.OPEN) {
			this.socket.close();
        }

		// 이벤트리스너 제거
		window.removeEventListener('popstate', handlePageLeave);
		window.removeEventListener('keydown', handleKeyPress);
	
		// 모달 관련 이벤트 리스너 제거
		if (this.modalConfirmBtn && this.modalConfirmBtnClickListener) {
			this.modalConfirmBtn.removeEventListener('click', this.modalConfirmBtnClickListener);
			this.modalConfirmBtnClickListener = null;
		}
	}
	
	render() {
		this.el.innerHTML = renderGame();
		
		// 게임 설정들 초기화
		this.canvas = this.el.querySelector('#gameCanvas');
		this.ctx = this.canvas.getContext('2d');

		// canvas 초기화 플래그
		this.isCanvasInitialized = true; 

		// 모달 초기화
		initializeModal(this);
		initializeResultModal(this);
	}

	// 메인 화면으로 이동
	redirectToMain() {
		window.location.href = '#/main';  // 메인 화면의 URL로 변경
    }
}
