// Websocket 요청 Url 생성
export function getWebsocketUrl(game) {
    const { protocol, hostname, hash } = location;

	// protocol 설정
    const wsProtocol = protocol === 'https:' ? 'wss' : 'ws';

	// 게임 타입 설정
	const gameType = hash === '#/game/onetoone/' ? 'onetoone' : 'tournament';
	game.gameType = gameType;

    const wsUrl = `${wsProtocol}://${hostname}/ws/${gameType}/`;

    return wsUrl;
}