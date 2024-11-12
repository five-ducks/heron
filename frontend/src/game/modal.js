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
		game.redirectToMain(); // 확인 버튼 클릭 시 메인 화면으로 이동
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

	// 확인 버튼 클릭 시 메인 화면으로 이동
	game.resultConfirmBtn.addEventListener('click', () => {
		hideResultModal(game);
		game.redirectToMain();  // 메인 화면으로 이동
	});
}

export function showDisconnectModal(game, message) {
	// 모달 요소가 없으면 초기화
	if (!game.modal || !game.modalMessage) {
		game.initializeModal(game);
	}
	
	// 모달 표시
	try {
		game.modalMessage.textContent = message;
		game.modal.style.display = 'block';
		game.modalVisible = true;
	} catch (error) {
		console.error("Error showing modal:", error);
	}
}

export function showResultModal(game, isWinner) {
	// 승리 여부에 따라 메시지 설정
	const message = isWinner ? 'WIN' : 'LOSE';
	game.resultMessage.textContent = message;
	
	// 모달 표시
	game.resultModal.style.display = 'block';
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