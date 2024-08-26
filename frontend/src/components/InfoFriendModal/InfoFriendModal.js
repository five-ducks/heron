import { Modal } from "../../core/modal.js";
import { MatchRecord } from "../MatchRecord/MatchRecord.js";

export class InfoFriendModal extends Modal {
    constructor(onClose = () => {}) {
        const content = /*html*/`
            <h1 class="title">친구 정보</h1>
            <div class="info_match">here</div>
        `;
        super(content, onClose);
    }
    render() {
        this.el.classList.add("info_friend_modal");
        const matchRecord = new MatchRecord();
        // this.el.querySelector(".info_match").append(matchRecord.el);
        // this.el.querySelector(".info_match").append(new MatchRecord().el);
    }
}
