import { Modal } from "../core/modal.js";

export class JoinModal extends Modal {
	constructor(onClose = () => {}) {
		const content = /*html*/`
			<h1>JOIN</h1>
			<div class="input_row">
				<input type="text" placeholder="Nickname">
				<input type="password" placeholder="Password">
				<input type="password" placeholder="Confirm Password">
			</div>
			<button id="modalSignUpButton">Sign Up</button>
		`;

		super(content, onClose);
	}
}
