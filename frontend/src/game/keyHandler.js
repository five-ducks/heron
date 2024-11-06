export function handleKeyPress(e, game) {
	if (!game.isGameStarted) {
		return;
	}
	
	let movement = null;
	if ((game.playerNumber === 1 && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) ||
	(game.playerNumber === 2 && (e.key === 'ArrowUp' || e.key === 'ArrowDown'))) {
		movement = { direction: e.key === 'ArrowUp' ? 'up' : 'down', player: game.playerNumber };
	}

	if (movement && game.socket.readyState === WebSocket.OPEN) {
		game.socket.send(JSON.stringify({ type: 'move', ...movement }));
	}
}