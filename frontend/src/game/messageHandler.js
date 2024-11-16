import { showDisconnectModal, showResultModal } from "./modal.js"

export function handleServerMessage(game, data) {
    switch(data.type) {
		case "connectionSuccess":
            handleConnection(game);
            break;
        case "gameState":
            game.gameState = data.state;
            break;
        case 'gameStart':
			game.startOnetoonetGame(data);
            break;
        case 'opponentDisconnected':
            showDisconnectModal(game, data.message);
            break;
        case 'gameEnd':
            showResultModal(game, data.winner === game.playerNumber);
            break;
        default:
            console.log('Unknown message type:', data.type);
    }
}

async function handleConnection(game) {
    try {
        // 유저 정보 가져오기
        game.userInfo = await getUserInfo();
		console.log(game.userInfo);

        // 웹소켓으로 유저 정보 전송
        game.socket.send(JSON.stringify({
            type: 'user_info',
            user_info: game.userInfo,
        }));

    } catch (error) {
        console.error('Error fetching user info:', error);
    }
}

async function getUserInfo() {
    try {
        const response = await fetch('/api/users/self/', {
            method: 'GET',
            credentials: 'include',  // 쿠키 포함
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch user info');
        }

        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}