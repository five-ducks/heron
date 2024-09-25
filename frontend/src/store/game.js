import { Store } from "../core/core.js";

const store = new Store({
	gameRecords: [],
	userInfo: {},
});

export default store;

export const loadGameRecords = async () => {
	try {
		const response = await fetch('https://localhost/src/temp/gameRecords.json');
		store.state.gameRecords = await response.json();
	} catch (error) {
		console.error('Error loading game records:', error);
	}
}

export const loadUserInfo = async () => {
	try {
		const response = await fetch('/api/users/self');
		store.state.userInfo = await response.json();

		if (response.status === 200) {
			console.log('User info updated successfully');
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
