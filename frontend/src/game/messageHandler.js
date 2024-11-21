import { showDisconnectModal, showResultModal, showSemifinalResultModal } from "./modal.js"

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
			if (data.winner === game.playerNumber) {
				showResultModal(game, 'WIN');
			}
			else {
				showResultModal(game, 'LOSE');
			}
            break;
		case 'semifinalResult':
			handleSemifinalResult(game, data);
            break;
        case 'finalResult':
            handleFinalResult(game, data);
            break;
        default:
            console.log('Unknown message type:', data.type);
    }
}

async function handleConnection(game) {
    try {
        // 유저 정보 가져오기
        game.userInfo = await getUserInfo();

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
            credentials: 'include',
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

function handleSemifinalResult(game, data) {
    if (data.result === 'win') {
		showSemifinalResultModal(game, data.result);
	} else {
		showSemifinalResultModal(game, data.result);
	}
}

function handleFinalResult(game, data) {
    if (data.result === 'win') {
        showResultModal(game, 'Champion!');
    } else {
        showResultModal(game, 'Runner-up');
    }
}