import { Modal } from "../Modal/index.js";
import { FriendGameRecords } from "../FriendGameRecords/FriendGameRecords.js";

export class InfoFriendModal extends Modal {
    constructor(props, onClose) {
        const name = props.username;
        const content = /*html*/`
            <h1 class="title">친구 정보</h1>
            <div class="friend_info">
                <div class="friend_name">이름: ${name}</div>
                <div class="friend_level">레벨: 0</div>
                <div class="friend_winrate">승률: 75%</div>
            </div>
            <div class="info_record"></div>
        `;
        super(content, onClose);
        this.userinfo = props;

        this.el.classList.add("info_friend_modal");

        const matchRecordList = this.el.querySelector(".info_record");
        const gameRecords = new FriendGameRecords();
        gameRecords.render(this.userinfo.matches, this.userinfo.username, this.userinfo.profile_img);// 
        matchRecordList.appendChild(gameRecords.el);


        this.render();
    }

    render() {
        // 추가적인 렌더링 로직이 필요할 경우 이곳에 작성
    }
}
