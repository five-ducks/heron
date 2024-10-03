import { Store } from "../core/core.js";

const store = new Store({
	gameRecords: [],
	userInfo: {},
	userFriends: [],
});

export default store;

export const loadGameRecords = async () => {
	try {
		const response = await fetch('/api/users/self');
		if (response.status === 200)
		{
			const user = await response.json();
			store.state.gameRecords = user.matches
		}
		else if (response.status === 403)
		{
			console.error('Forbidden:', response.error);
		}
		else
			console.error('Unknown error:', response.error);
	} catch (error) {
		console.error('Error loading game records:', error);
	}
}

export const loadUserInfo = async () => {
	try {
		const response = await fetch('/api/users/self');
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
