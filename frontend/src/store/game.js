import { Store } from "../core/core.js";

const store = new Store({
    userInfo: {},
    userGameRecords: [],
    userFriends: [],
    userFriendGameRecords: [],
    currentView: localStorage.getItem('currentView') || 'selectPage',
});

export default store;

// 친구들의 게임 기록을 불러오는 함수
export const loadFriendGameRecords = async () => {
    return new Promise(async (resolve, reject) => {
        try {
            const friendList = store.state.userFriends;
            const response = await fetch(`/api/matches/search/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ friendList }),
            });
            if (response.status === 200) {
                const user = await response.json();
                store.state.userFriendGameRecords = user.matches;
                resolve(user.matches);
            } else if (response.status === 403) {
                console.error('Forbidden:', response.error);
                reject(new Error('Forbidden'));
            } else {
                console.error('Unknown error:', response.error);
                reject(new Error('Unknown error'));
            }
        } catch (error) {
            console.error('Error loading game records:', error);
            reject(error);
        }
    });
}

// 사용자의 게임 기록을 불러오는 함수
export const loaduserGameRecords = async () => {
    return new Promise(async (resolve, reject) => {
        try {
            const response = await fetch(`/api/matches/${store.state.userInfo.username}/`);
            if (response.status === 200) {
                const user = await response.json();
                store.state.userGameRecords = user.matches;
                resolve(user.matches);
            } else if (response.status === 403) {
                console.error('Forbidden:', response.error);
                reject(new Error('Forbidden'));
            } else {
                console.error('Unknown error:', response.error);
                reject(new Error('Unknown error'));
            }
        } catch (error) {
            console.error('Error loading game records:', error);
            reject(error);
        }
    });
}

// 사용자의 친구 목록을 불러오는 함수
export const loadUserFriends = async () => {
    return new Promise(async (resolve, reject) => {
        try {
            const response = await fetch(`/api/users/self/friends/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
            });
            const friendsInfo = await response.json();
            if (response.ok) {
                console.log('친구 목록을 가져오는 데 성공했습니다:', friendsInfo);
                store.state.userFriends = friendsInfo;
                await loadFriendGameRecords();
                resolve(friendsInfo);
            } else {
                console.error('친구 목록을 가져오는 중 오류 발생:', friendsInfo.error);
                reject(new Error(friendsInfo.error));
            }
        } catch (error) {
            console.error('친구 목록을 가져오는 중 오류 발생:', error);
            reject(error);
        }
    });
}

// 사용자의 정보를 불러오는 함수
export const loadUserInfo = async () => {
    return new Promise(async (resolve, reject) => {
        try {
            const response = await fetch('/api/users/self/');
            if (response.status === 200) {
                const userInfo = await response.json();
                store.state.userInfo = userInfo;
                resolve(userInfo);
            } else if (response.status === 403) {
                console.error('Forbidden:', response.error);
                reject(new Error('Forbidden'));
            } else {
                console.error('Unknown error:', response.error);
                reject(new Error('Unknown error'));
            }
        } catch (error) {
            console.error('Error loading user info:', error);
            reject(error);
        }
    });
}