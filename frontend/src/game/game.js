import { Component } from "../core/core.js";

// Websocket 요청 Url 생성
function getWebsocketUrl(gameType) {
    const { protocol, hostname, port } = location;

	// protocol 설정
    const wsProtocol = protocol === 'https:' ? 'wss' : 'ws';

	// port 설정
    const wsPort = port ? `:${port}` : '';

	// 게임 타입 설정
	const path = gameType === 'onetoone' ? 'onetoone' : 'tournament';

    const wsUrl = `${wsProtocol}://${hostname}/ws/onetoone/`;
    return wsUrl;
}

export class PingPongGame extends Component {
    constructor(payload = {}) {
        super(payload);
		this.gameType = 'onetoone';
        this.socket = null;
        this.canvas = null;
        this.ctx = null;
        this.gameState = {
            ball: { x: 400, y: 300, radius: 10 },
            paddle1: { x: 10, y: 250, width: 10, height: 100 },
            paddle2: { x: 780, y: 250, width: 10, height: 100 },
            score: { player1: 0, player2: 0 }
        };
        this.lastUpdateTime = 0;
        this.isGameStarted = false;
        this.playerSide = null;
		this.modalVisible = false;

        // 페이지 이동 이벤트리스너
        this.handlePageLeave = this.handlePageLeave.bind(this);
        window.addEventListener('popstate', this.handlePageLeave);

		// 새로고침 이벤트리스너
        this.handleBeforeUnload = this.handleBeforeUnload.bind(this);
        window.addEventListener('beforeunload', this.handleBeforeUnload);

        this.initializeWebSocket();
    }

    initializeWebSocket() {
        this.socket = new WebSocket(getWebsocketUrl(this.gameType));

		// socket 연결 성공
        this.socket.onopen = () => {
			this.updateStatus('Connected, waiting for opponent...');
        };
		// socket message 처리
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleServerMessage(data);
        };
		// socket 연결 종료
        this.socket.onclose = (event) => {
            if (event.wasClean) { // 정상정료시 true
                this.updateStatus('Closed cleanly');
            } else {
                this.updateStatus('Connection died');
            }
        };

		// socket 에러
        this.socket.onerror = (error) => {
            this.updateStatus('Error: ' + error.message);
        };

		window.addEventListener('keydown', this.handleKeyPress.bind(this));
    }

	handleServerMessage(data) {
		switch(data.type) {
			case 'gameState':
				this.gameState = data.state;
				break;
			case 'gameStart':
				this.render();  // gameStart 이벤트를 받을 때 렌더링
				this.gameState = data.state
				this.playerSide = data.side;
				this.playerNumber = data.player;
				this.setPlayerNicknames(data.player1Nickname, data.player2Nickname);
				this.startGame();
				break;
			case 'opponentDisconnected':
				this.showDisconnectModal(data.message);
				break;
			case 'gameEnd':
				this.showResultModal(data.winner === this.playerNumber);
           		break;
			default:
				console.log('Unknown message type:', data.type);
		}
	}
		
	startGame() {
		this.isGameStarted = true;
		
		const waitingScreen = this.el.querySelector('#waitingScreen');
		if (waitingScreen) {
			waitingScreen.style.display = 'none';
		} else {
			console.error("Waiting screen not found");
		}
	
		if (this.canvas) {
			this.canvas.style.display = 'block';
		} else {
			console.error("Canvas not found");
		}
		
		this.updateStatus(`Game Started! You are the ${this.playerSide} player.`);
		requestAnimationFrame(this.gameLoop.bind(this));
	}
	
    gameLoop(timestamp) {
        if (!this.isGameStarted) {
			return;
		}
		
        const deltaTime = timestamp - this.lastUpdateTime;
        this.lastUpdateTime = timestamp;
		
        this.draw(deltaTime);
        requestAnimationFrame(this.gameLoop.bind(this));
    }

    // 컴포넌트가 제거될 때 호출되는 메서드
    destroy() {
		// socket 연결 종료
		this.closeWebSocket();
	
		// 이벤트리스너 제거
		window.removeEventListener('popstate', this.handlePageLeave);
		window.removeEventListener('beforeunload', this.handleBeforeUnload);
		window.removeEventListener('keydown', this.handleKeyPress.bind(this));
	
		// 모달 관련 이벤트 리스너 제거
		if (this.modalConfirmBtn && this.modalConfirmBtnClickListener) {
			this.modalConfirmBtn.removeEventListener('click', this.modalConfirmBtnClickListener);
			this.modalConfirmBtnClickListener = null;
		}
	}

	// 메인 화면으로 이동
	redirectToMain() {
		window.location.href = '#/main';  // 메인 화면의 URL로 변경
    }

	// 페이지 이동(뒤로가기) 처리
	handlePageLeave() {
		// 서버에 disconnect 메시지 전송
		if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        	this.socket.send(JSON.stringify({
				type: 'disconnect',
			}));
    	}
		this.closeWebSocket();
	}

    // 새로고침 처리
	handleBeforeUnload() {
    	// 서버에 disconnect 메시지 전송
   		if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        	this.socket.send(JSON.stringify({
				type: 'disconnect',
			}));
    	}
    	this.closeWebSocket();
	}


    // socket 연결 종료 메서드
    closeWebSocket() {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
			this.socket.close();
        }
    }
	
    handleKeyPress(e) {
		if (!this.isGameStarted) {
			return;
		}
		
		let movement = null;
		if ((this.playerNumber === 1 && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) ||
		(this.playerNumber === 2 && (e.key === 'ArrowUp' || e.key === 'ArrowDown'))) {
			movement = { direction: e.key === 'ArrowUp' ? 'up' : 'down', player: this.playerNumber };
		}
	
		if (movement && this.socket.readyState === WebSocket.OPEN) {
			this.socket.send(JSON.stringify({ type: 'move', ...movement }));
		}
	}

    showDisconnectModal(message) {
        // 모달 요소가 없으면 초기화
        if (!this.modal || !this.modalMessage) {
			this.initializeModal();
        }
		
        // 모달 표시
        try {
			this.modalMessage.textContent = message;
            this.modal.style.display = 'block';
            this.modalVisible = true;
        } catch (error) {
            console.error("Error showing modal:", error);
        }
    }

    hideModal() {
		if (this.modal) {
			this.modal.style.display = 'none';
			this.modalVisible = false;
		} else {
			console.error("Cannot hide modal: modal element not found");
		}
	}
		
    draw(deltaTime) {
		if (!this.ctx || !this.isGameStarted) {
			return;
		}
		
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.fillStyle = 'black';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
		
        this.ctx.fillStyle = 'white';
        this.ctx.fillRect(this.gameState.paddle1.x, this.gameState.paddle1.y, this.gameState.paddle1.width, this.gameState.paddle1.height);
        this.ctx.fillRect(this.gameState.paddle2.x, this.gameState.paddle2.y, this.gameState.paddle2.width, this.gameState.paddle2.height);
		
        this.ctx.beginPath();
        this.ctx.arc(this.gameState.ball.x, this.gameState.ball.y, this.gameState.ball.radius, 0, Math.PI * 2);
        this.ctx.fillStyle = 'white';
        this.ctx.fill();
        this.ctx.closePath();
		
        this.ctx.font = '30px Arial';
        this.ctx.fillText(this.gameState.score.player1, this.canvas.width / 4, 50);
        this.ctx.fillText(this.gameState.score.player2, 3 * this.canvas.width / 4, 50);
    }
	
	render() {
		this.el.innerHTML = `
		<div class="game-container">
		<h1>PingPong Game</h1>
		<div id="status"></div>
		<div id="waitingScreen" style="display: block;">
		<h2>Waiting for opponent...</h2>
		</div>
		<canvas id="gameCanvas" width="800" height="600" style="border: 1px solid black; display: none;"></canvas>
		
		<!-- 플레이어 닉네임 표시 -->
		<div class="nickname-container">
		<div id="player1Nickname" class="nickname"></div>
		<div id="player2Nickname" class="nickname"></div>
		</div>
		
		<!-- 기존의 연결 종료 모달 -->
		<div id="disconnectModal" class="modal" style="display: none;">
		<div class="modal-content">
		<p id="modalMessage"></p>
		<button id="modalConfirmBtn">확인</button>
		</div>
		</div>
		
		<!-- 결과 모달 추가 -->
		<div id="resultModal" class="modal" style="display: none;">
		<div class="modal-content">
		<h1 id="resultMessage"></h1>
		<button id="resultConfirmBtn">확인</button>
		</div>
		</div>
		</div>
		
		<style>
		.nickname-container {
			display: flex;
			justify-content: space-between;
			margin: 10px 0;
			}
			
			.nickname {
				font-size: 20px;
				font-weight: bold;
				width: 50%;
				text-align: center;
				}
				
				.modal {
					display: none;
					position: fixed;
					z-index: 1;
					left: 0;
					top: 0;
					width: 100%;
					height: 100%;
					background-color: rgba(0, 0, 0, 0.5);
					}
					
					.modal-content {
						background-color: #fefefe;
						margin: 15% auto;
						padding: 20px;
						border: 1px solid #888;
						width: 300px;
						text-align: center;
						border-radius: 5px;
						}
						
						#resultConfirmBtn {
							margin-top: 15px;
							padding: 10px 20px;
					background-color: #4CAF50;
					color: white;
					border: none;
					border-radius: 3px;
					cursor: pointer;
					}
					
					#resultConfirmBtn:hover {
						background-color: #45a049;
						}
						</style>
						`;
						
						// 기존 게임 설정들 초기화
						this.canvas = this.el.querySelector('#gameCanvas');
						this.ctx = this.canvas.getContext('2d');
	
		// 모달 초기화
		this.initializeModal();
		this.initializeResultModal(); // 새로운 결과 모달 초기화
	}	

    initializeModal() {
		this.modal = this.el.querySelector('#disconnectModal');
		this.modalMessage = this.el.querySelector('#modalMessage');
		this.modalConfirmBtn = this.el.querySelector('#modalConfirmBtn');
		
		if (!this.modal || !this.modalMessage || !this.modalConfirmBtn) {
			console.error('Modal elements not found');
			return;
		}
	
		// 중복 등록 방지 코드 제거
		this.modalConfirmBtn.addEventListener('click', () => {
			this.hideModal();
			this.redirectToMain(); // 확인 버튼 클릭 시 메인 화면으로 이동
		});
	}

	initializeResultModal() {
		this.resultModal = this.el.querySelector('#resultModal');
		this.resultMessage = this.el.querySelector('#resultMessage');
		this.resultConfirmBtn = this.el.querySelector('#resultConfirmBtn');
		
		if (!this.resultModal || !this.resultMessage || !this.resultConfirmBtn) {
			console.error('Result modal elements not found');
			return;
		}
	
		// 확인 버튼 클릭 시 메인 화면으로 이동
		this.resultConfirmBtn.addEventListener('click', () => {
			this.hideResultModal();
			this.redirectToMain();  // 메인 화면으로 이동
		});
	}
	
	showResultModal(isWinner) {
		// 승리 여부에 따라 메시지 설정
		const message = isWinner ? 'WIN' : 'LOSE';
		this.resultMessage.textContent = message;
		
		// 모달 표시
		this.resultModal.style.display = 'block';
	}
	
	hideResultModal() {
		this.resultModal.style.display = 'none';
	}

	// player1이 본인, player2가 상대
	setPlayerNicknames(player1Nickname, player2Nickname) {
		const player1NicknameElement = this.el.querySelector('#player1Nickname');
		const player2NicknameElement = this.el.querySelector('#player2Nickname');
	
		if (this.playerSide === 'left') {
			player1NicknameElement.textContent = player1Nickname;
			player2NicknameElement.textContent = player2Nickname;
		} else {
			player1NicknameElement.textContent = player2Nickname;
			player2NicknameElement.textContent = player1Nickname;
		}
	}

	updateStatus(status) {
		this.el.querySelector('#status').innerHTML = status;
	}
}
