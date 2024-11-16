// 뒤로가기 처리
export function handlePageLeave(game) {
	var socket = game.socket;
	// 서버에 disconnect 메시지 전송
	if (socket && socket.readyState === WebSocket.OPEN) {
		socket.send(JSON.stringify({
			type: 'disconnect',
		}));
		socket.close();
	}
}

// 새로고침 처리
export function handlePageReload(game) {
	var socket = game.socket;
	// 서버에 disconnect 메시지 전송
	if (socket && socket.readyState === WebSocket.OPEN) {
		socket.send(JSON.stringify({
			type: 'disconnect',
		}));
		socket.close();
	}
	game.redirectToMain();
}