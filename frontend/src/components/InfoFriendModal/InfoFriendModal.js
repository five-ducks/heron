import { Modal } from "../Modal/index.js";
import { FriendGameRecords } from "../FriendGameRecords/FriendGameRecords.js";

export class InfoFriendModal extends Modal {
    constructor(props, onClose) {
        console.log(props);
        const name = props.username;
        const content = /*html*/`
            <div class="friend_info">
                <div class="friend_name">이름: ${name}</div>
                <div class="friend_level">레벨: 0</div>
                <div class="friend_winrate">승률: 75%</div>
            </div>
            <div class="info_record"></div>
        `;
        super('친구 정보', content, onClose);
        this.userinfo = props;

        this.el.classList.add("info_friend_modal");

        const matchRecordList = this.el.querySelector(".info_record");
        const gameRecords = new FriendGameRecords();
        gameRecords.render(this.userinfo.matches, this.userinfo.username, this.userinfo.profile_img);// 
        matchRecordList.appendChild(gameRecords.el);


        this.render();
    }

    // static getContent() {
    //     return /*html*/`
    //         <div class="friend_info">
    //             <div class="friend_name">이름: </div>
    //             <div class="friend_level">레벨: </div>
    //             <div class="friend_win
    //         </div>
    //         <div class="info_record"></div>
    //     `;
    // }

    calculateLevel(exp) {
        let level = 1;
        let expForNextLevel = ProfileLevel.BASE_EXP; // 클래스 변수 접근 시 ProfileLevel 사용

        while (exp >= expForNextLevel) {
            exp -= expForNextLevel; // 다음 레벨로 가기 위해 필요한 exp 차감
            level++; // 레벨 업
            expForNextLevel = Math.floor(expForNextLevel * ProfileLevel.EXP_MULTIPLIER); // 다음 레벨에 필요한 exp 증가
        }

        return level;
    }

    render() {
        // 추가적인 렌더링 로직이 필요할 경우 이곳에 작성
    }
}
