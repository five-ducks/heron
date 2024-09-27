import { Component } from "../core/core.js";

// Websocket 요청 Url 생성
function getWebsocketUrl(path) {
    const { protocol, hostname, port } = location;

	// protocol 설정
    const wsProtocol = protocol === 'https:' ? 'wss' : 'ws';

	// port 설정
    const wsPort = port ? `:${port}` : '';

    const wsUrl = `${wsProtocol}://${hostname}/ws/online/onetoone/1/`;
    console.log(wsUrl);
    return wsUrl;
}

export class PingPongGame extends Component {
    constructor(payload = {}) {
        super(payload);
        this.gameId = 1;
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
        this.initializeWebSocket();
    }

    initializeWebSocket() {
        this.socket = new WebSocket(getWebsocketUrl(this.url));
        console.log("Waiting for Websocket Connecting....");

        this.socket.onopen = () => {
            console.log('WebSocket connected');
            this.updateStatus('Connected, waiting for opponent...');
        };
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleServerMessage(data);
        };
        this.socket.onclose = (event) => {
            if (event.wasClean) {
                this.updateStatus('Closed cleanly');
            } else {
                this.updateStatus('Connection died');
            }
            console.log('WebSocket disconnected');
        };
        this.socket.onerror = (error) => {
            this.updateStatus('Error: ' + error.message);
        };
    }

    render() {
        this.el.innerHTML = `
            <h1>PingPong Game ${this.gameId}</h1>
            <div id="status"></div>
            <div id="waitingScreen" style="display: block;">
                <h2>Waiting for opponent...</h2>
            </div>
            <canvas id="gameCanvas" width="800" height="600" style="border: 1px solid black; display: none;"></canvas>
        `;
        this.canvas = this.el.querySelector('#gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        window.addEventListener('keydown', this.handleKeyPress.bind(this));
    }

    handleServerMessage(data) {
		switch(data.type) {
			case 'gameState':
				// console.log('Received game state:', data.state);
				this.gameState = data.state;
				break;
			case 'gameStart':
				this.render();  // gameStart 이벤트를 받을 때 렌더링
				this.playerSide = data.side;
				this.playerNumber = data.player;
				this.startGame();
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
        if (!this.isGameStarted) return;

        const deltaTime = timestamp - this.lastUpdateTime;
        this.lastUpdateTime = timestamp;

        this.draw(deltaTime);
        requestAnimationFrame(this.gameLoop.bind(this));
    }

    draw(deltaTime) {
        if (!this.ctx || !this.isGameStarted) return;

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

    handleKeyPress(e) {
		if (!this.isGameStarted) return;
	
		let movement = null;
		if ((this.playerNumber === 1 && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) ||
			(this.playerNumber === 2 && (e.key === 'ArrowUp' || e.key === 'ArrowDown'))) {
			movement = { direction: e.key === 'ArrowUp' ? 'up' : 'down', player: this.playerNumber };
		}
	
		if (movement && this.socket.readyState === WebSocket.OPEN) {
			console.log('Sending movement:', movement);
			this.socket.send(JSON.stringify({ type: 'move', ...movement }));
		}
	}

    updateStatus(status) {
        this.el.querySelector('#status').innerHTML = status;
    }
}