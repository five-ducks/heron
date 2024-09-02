import { Store } from "../core/core.js";

const store = new Store({
	gameRecords: [],
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