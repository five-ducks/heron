export function renderGame() {
	return `
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
}

export function draw(game) {
	if (!game.ctx || !game.isGameStarted) {
		return;
	}
	
	game.ctx.clearRect(0, 0, game.canvas.width, game.canvas.height);
	game.ctx.fillStyle = 'black';
	game.ctx.fillRect(0, 0, game.canvas.width, game.canvas.height);
	
	game.ctx.fillStyle = 'white';
	game.ctx.fillRect(game.gameState.paddle1.x, game.gameState.paddle1.y, game.gameState.paddle1.width, game.gameState.paddle1.height);
	game.ctx.fillRect(game.gameState.paddle2.x, game.gameState.paddle2.y, game.gameState.paddle2.width, game.gameState.paddle2.height);
	
	game.ctx.beginPath();
	game.ctx.arc(game.gameState.ball.x, game.gameState.ball.y, game.gameState.ball.radius, 0, Math.PI * 2);
	game.ctx.fillStyle = 'white';
	game.ctx.fill();
	game.ctx.closePath();
	
	game.ctx.font = '30px Arial';
	game.ctx.fillText(game.gameState.score.player1, game.canvas.width / 4, 50);
	game.ctx.fillText(game.gameState.score.player2, 3 * game.canvas.width / 4, 50);
}

// player1이 본인, player2가 상대
export function setPlayerNicknames(game, player1Nickname, player2Nickname) {
	const player1NicknameElement = game.el.querySelector('#player1Nickname');
	const player2NicknameElement = game.el.querySelector('#player2Nickname');

	if (game.playerSide === 'left') {
		player1NicknameElement.textContent = player1Nickname;
		player2NicknameElement.textContent = player2Nickname;
	} else {
		player1NicknameElement.textContent = player2Nickname;
		player2NicknameElement.textContent = player1Nickname;
	}
}

export function updateStatus(game, status) {
	game.el.querySelector('#status').innerHTML = status;
}