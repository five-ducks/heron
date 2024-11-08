let statusSockets = [];

export const startWebSocketConnection = (username) => {
    const existingSocketIndex = statusSockets.findIndex(socketObj => socketObj.username === username);

    if (existingSocketIndex !== -1) {
        const existingSocket = statusSockets[existingSocketIndex].socket;
        statusSockets.splice(existingSocketIndex, 1);
        console.log(`Existing WebSocket for user ${username} closed and removed.`);
    }
    // 브라우저의 강제 종료로 인해 websocket이 닫힌 경우, 재 로그인을 진행할때 statausSockets 배열에서 이전에 지우지 못한 소켓을 삭제

    const socket = new WebSocket('wss://localhost/ws/status/');

    socket.onopen = () => {
        console.log("WebSocket connection opened.");
    };

    socket.onclose = () => {
        console.log("WebSocket connection closed.");
    };
    // 웹소켓의 연결과 끊어짐을 로그로 남기기 위한 용도

    statusSockets.push({ username, socket });
    // statusSockets 배열에 key: value 형식으로 websocket 추가
};

export const closeWebSocketConnection = (username) => {
    const socketIndex = statusSockets.findIndex(socketObj => socketObj.username === username);

    if (socketIndex !== -1) {
        const socket = statusSockets[socketIndex].socket;
        socket.close();
        statusSockets.splice(socketIndex, 1);
        console.log(`WebSocket for user ${username} closed and removed from statusSockets.`);
    }
};
// logout 이후 정상적인 종료일 때 websocket 을 닫고 배열에서 삭제