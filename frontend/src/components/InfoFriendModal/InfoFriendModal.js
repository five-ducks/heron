import { Modal } from "../../core/modal.js";
import { MatchRecord } from "../MatchRecord/MatchRecord.js";

export class InfoFriendModal extends Modal {
    constructor(onClose = () => {}) {
        const content = /*html*/`
            <h1 class="title">친구 정보</h1>
            <div class="info_record"></div>
        `;
        super(content, onClose);
        
        this.el.classList.add("info_friend_modal");
        const matchRecordList = this.el.querySelector(".info_record");
        const matchRecord = new MatchRecord();
        matchRecordList.appendChild(matchRecord.el);
        this.render();
    }
    render() {
    }
}
