import { Modal } from "../Modal/index.js";
import { FriendGameRecords } from "../FriendGameRecords/FriendGameRecords.js";
import { loadFriendGameRecords } from "../../store/game.js";
export class InfoFriendModal extends Modal {
    constructor(props) {
        const name = props.username;
        const level = InfoFriendModal.calculateLevel(props.exp);
        const winrate = InfoFriendModal.calculateWinrate(props.win_cnt, props.lose_cnt);
        super('친구 정보', InfoFriendModal.getContent(name, level, winrate));
        
        this.userinfo = props;
        this.el.classList.add("info_friend-modal");
        this.renderAdditionalContent(name);
    }

    async renderAdditionalContent(name) {
        const matchRecordList = this.el.querySelector(".info-record");
		await loadFriendGameRecords();
        const gameRecords = new FriendGameRecords();
        gameRecords.recoredsRender(name);
        matchRecordList.appendChild(gameRecords.el);
    }

    static getContent(name = '이름', level = '레벨', winrate = 'win률') {
        return /*html*/`
            <div class="friend-info">
                <div class="friend-name">이름: ${name}</div>
                <div class="friend-level">레벨: ${level}</div>
                <div class="friend-winrate">승률: ${winrate}%</div>
            </div>
            <div class="info-record"></div>
        `;
    }

    static calculateWinrate(win, lose) {
        const total = win + lose;
        if (total === 0)
            return 0; // 게임을 하지 않았다면 0% win률 반환
        return Math.round((win / total) * 100);
    }

	// 레벨당 필요한 exp 양 계산 함수
	static BASE_EXP = 1000; // 레벨당 기본 exp
	static EXP_MULTIPLIER = 1.5; // 레벨당 증가하는 exp 배율

    static calculateLevel(exp) {
        let level = 1;
        let expForNextLevel = InfoFriendModal.BASE_EXP; // 클래스 변수 접근 시 ProfileLevel 사용

        while (exp >= expForNextLevel) {
            exp -= expForNextLevel; // 다음 레벨로 가기 위해 필요한 exp 차감
            level++; // 레벨 업
            expForNextLevel = Math.floor(expForNextLevel * InfoFriendModal.EXP_MULTIPLIER); // 다음 레벨에 필요한 exp 증가
        }

        return level;
    }
}