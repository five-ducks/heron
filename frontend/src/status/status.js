let statusSocket = null;

export const startWebSocketConnection = () => {
    if (statusSocket) {
        statusSocket.close();
        console.log("Existing WebSocket connection closed.");
    }
    // 브라우저의 강제 종료로 인해 websocket이 닫힌 경우, 재 로그인을 진행할때 statausSockets 배열에서 이전에 지우지 못한 소켓을 삭제

    statusSocket = new WebSocket('wss://localhost/ws/status/');

    statusSocket.onopen = () => {
        console.log("WebSocket connection opened.");
    };
    // 웹소켓과 연결됨을 로그로 알림

    statusSocket.onclose = () => {
        console.log("WebSocket connection closed.");
    };
    // 웹소켓과 연결이 끊어짐을 로그로 알림
};

export const closeWebSocketConnection = () => {
    if (statusSocket) {
        statusSocket.close();
        statusSocket = null;
        console.log("WebSocket connection closed and reset.");
    }
};
// logout 이후 정상적인 종료일 때 websocket 을 닫고 배열에서 삭제