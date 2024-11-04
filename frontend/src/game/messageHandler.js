import { showDisconnectModal, showResultModal } from "./modal.js"

export function handleServerMessage(game, data) {
    switch(data.type) {
        case "gameState":
            game.gameState = data.state;
            break;
        case 'gameStart':
            game.startGame(data);
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