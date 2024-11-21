export function initializeModal(game) {
    game.modal = game.el.querySelector('#disconnectModal');
    game.modalMessage = game.el.querySelector('#modalMessage');
    game.modalConfirmBtn = game.el.querySelector('#modalConfirmBtn');
    
    if (!game.modal || !game.modalMessage || !game.modalConfirmBtn) {
        console.error('Modal elements not found');
        return;
    }

    game.modalConfirmBtn.addEventListener('click', () => {
        hideModal(game);
        game.redirectToMain();
    });
}

export function initializeResultModal(game) {
    game.resultModal = game.el.querySelector('#resultModal');
    game.resultMessage = game.el.querySelector('#resultMessage');
    game.resultConfirmBtn = game.el.querySelector('#resultConfirmBtn');
    
    if (!game.resultModal || !game.resultMessage || !game.resultConfirmBtn) {
        console.error('Result modal elements not found');
        return;
    }
}

export function showDisconnectModal(game, message) {
    if (!game.modal || !game.modalMessage) {
        game.initializeModal(game);
    }
    
    try {
        game.modalMessage.textContent = message;
        game.modal.style.display = 'block';
        game.modalVisible = true;
    } catch (error) {
        console.error("Error showing modal:", error);
    }
}

export function showResultModal(game, result) {
    game.resultMessage.textContent = result;
    game.resultModal.style.display = 'block';

    // 기존 이벤트 리스너 제거
    game.resultConfirmBtn.replaceWith(game.resultConfirmBtn.cloneNode(true));
    game.resultConfirmBtn = game.el.querySelector('#resultConfirmBtn');

    // 새 이벤트 리스너 등록
    game.resultConfirmBtn.addEventListener('click', () => {
        hideResultModal(game);
        game.redirectToMain();
    }, { once: true });
}

export function showSemifinalResultModal(game, result) {
    game.gameType = 'semifinal';
    game.lastResult = result;
    
    game.resultMessage.textContent = result === 'win' ? 'READY' : 'LOSE';
    game.resultModal.style.display = 'block';

    // 기존 이벤트 리스너 제거
    game.resultConfirmBtn.replaceWith(game.resultConfirmBtn.cloneNode(true));
    game.resultConfirmBtn = game.el.querySelector('#resultConfirmBtn');

    // 새 이벤트 리스너 등록
    game.resultConfirmBtn.addEventListener('click', () => {
        if (result === 'win') {
            game.socket.send(JSON.stringify({
                type: 'ready',
            }));
        } else {
            game.redirectToMain();
        }
        hideResultModal(game);
    }, { once: true });
}

export function showFinalResultModal(game, result) {
    game.gameType = 'final';
    game.lastResult = result;
    
    game.resultMessage.textContent = result === 'win' ? 'VICTORY!' : 'RUNNER-UP';
    game.resultModal.style.display = 'block';

    // 기존 이벤트 리스너 제거
    game.resultConfirmBtn.replaceWith(game.resultConfirmBtn.cloneNode(true));
    game.resultConfirmBtn = game.el.querySelector('#resultConfirmBtn');

    // 새 이벤트 리스너 등록
    game.resultConfirmBtn.addEventListener('click', () => {
        game.redirectToMain();
        hideResultModal(game);
    }, { once: true });
}

export function hideModal(game) {
    if (game.modal) {
        game.modal.style.display = 'none';
        game.modalVisible = false;
    } else {
        console.error("Cannot hide modal: modal element not found");
    }
}

export function hideResultModal(game) {
    game.resultModal.style.display = 'none';
}