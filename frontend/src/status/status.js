let statusSocket = null;

export const startWebSocketConnection = () => {
    if (!getSocketStatus()) {
        statusSocket = null;
        statusSocket = new WebSocket(getWebsocketUrl());
    }
    return new Promise((resolve) => {
        statusSocket.onopen = () => {
            console.log("WebSocket connection opened.");
            resolve(true); // WebSocket 연결이 열렸을 때 resolve 호출
        };

        statusSocket.onclose = () => {
            console.log("WebSocket connection closed.");
            resolve(true); // WebSocket 연결이 끊어졌을 때 resolve 호출
        };

        statusSocket.onerror = () => {
            console.log("Websocket connection failed.");
            resolve(true);
        };

        if (getSocketStatus())
            resolve(true);
    });
};

export const closeWebSocketConnection = () => {
    if (statusSocket) {
        statusSocket.close();
        statusSocket = null;
        console.log("WebSocket connection reset.");
    }
};
// logout 이후 정상적인 종료일 때 websocket 을 닫고 배열에서 삭제

export const getSocketStatus = () => {
    return statusSocket !== null && statusSocket.readyState === WebSocket.OPEN;
};

export function getWebsocketUrl() {
    const { protocol, hostname } = location;

    // protocol 설정
    const wsProtocol = protocol === 'https:' ? 'wss' : 'ws';

    // 게임 타입 설정
    const wsUrl = `${wsProtocol}://${hostname}/ws/status/`;

    return wsUrl;
}