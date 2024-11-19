import { GameRecords } from "../components/GameRecords/GameRecords.js";
import { Store } from "../core/core.js";

const store = new Store({
	userInfo: {},
	userGameRecords: [],
	gameRecords: [], // (구)
	userFriends: [],
	userFriendGameRecords: [],
});

export default store;

// 친구들의 게임 기록을 불러오는 함수 (요청 미구현)
export const loadFriendGameRecords = async () => {
	try {
		// 갖고 있는 친구 목록으로 친구들의 게임 기록을 불러옵니다.
		const friendList = store.state.userFriends;
		const response = await fetch(`/api/matches/friend/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ friendList }),
		});
		if (response.status === 200) {
			const user = await response.json();
			store.state.userFriendGameRecords = user.matches
		}
		else if (response.status === 403) {
			console.error('Forbidden:', response.error);
		}
		else
			console.error('Unknown error:', response.error);
	} catch (error) {
		console.error('Error loading game records:', error);
	}
}

// 사용자의 게임 기록을 불러오는 함수
export const loaduserGameRecords = async () => {
	try {
		const response = await fetch(`/api/matches/${store.state.userInfo.username}/`);
		if (response.status === 200) {
			const user = await response.json();
			store.state.userGameRecords = user.matches
		}
		else if (response.status === 403) {
			console.error('Forbidden:', response.error);
		}
		else
			console.error('Unknown error:', response.error);
	} catch (error) {
		console.error('Error loading game records:', error);
	}
}

// 사용자의 친구 목록을 불러오는 함수
export const loadUserFriends = async () => {
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
		} else {
			console.error('친구 목록을 가져오는 중 오류 발생:', friendsInfo.error);
		}

		// 가져온 친구 목록을 Store의 userFriends 상태에 저장합니다.
		store.state.userFriends = friendsInfo;
		loadFriendGameRecords();

	} catch (error) {
		console.error('친구 목록을 가져오는 중 오류 발생:', error);
	}
}

// 사용자 게임 기록을 불러오는 함수 (구)
export const loadGameRecords = async () => {
	try {
		const response = await fetch('/api/users/self/');
		if (response.status === 200) {
			const user = await response.json();
			store.state.gameRecords = user.matches
		}
		else if (response.status === 403) {
			console.error('Forbidden:', response.error);
		}
		else
			console.error('Unknown error:', response.error);
	} catch (error) {
		console.error('Error loading game records:', error);
	}
}

// 사용자의 정보를 불러오는 함수
export const loadUserInfo = async () => {
	try {
		const response = await fetch('/api/users/self/');
		if (response.status === 200) {
			store.state.userInfo = await response.json();
		}
		else if (response.status === 403) {
			console.error('Forbidden:', response.error);
		}
		else
			console.error('Unknown error:', response.error);
	} catch (error) {
		console.error('Error loading user info:', error);
	}
}