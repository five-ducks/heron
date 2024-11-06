// 페이지 이동(뒤로가기, 새로고침) 처리
export function handlePageLeave(socket) {
	// 서버에 disconnect 메시지 전송
	if (socket && socket.readyState === WebSocket.OPEN) {
		socket.send(JSON.stringify({
			type: 'disconnect',
		}));
		socket.close();
	}
}
