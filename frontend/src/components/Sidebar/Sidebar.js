import { Component } from "../../core/core.js";
import { FriendProfile } from "../Profile/FriendProfile.js";
import { InfoFriendModal } from "../InfoFriendModal/InfoFriendModal.js";
import { getCookie } from "../../core/core.js";

export class Sidebar extends Component {
    // Store의 userInfo를 받아옵니다.
    constructor(props) {
        super();
        this.userInfo = props;

        // 친구 목록을 불러오기 위해 fetchFriends 함수를 호출합니다.
        this.friendRender(this.userInfo);
    }
    friendRender(userInfo) {
        this.el.classList.add('friendwindow');
        this.el.innerHTML = /*html*/`
            <button class="addfriend">친구추가 +</button>
            <div class="friends"></div>
        `;

        const fetchFriends = async () => {
            const allUrl = `/api/users/self/friends`;
            try {
                const response = await fetch(allUrl, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                });
                const friendsInfo = await response.json();

                // 가져온 친구 목록을 반복하면서 FriendProfile 컴포넌트를 생성합니다.
                friendsInfo.forEach(friendData => {
                    console.log("data", friendData);
                    const friend = new FriendProfile(friendData.username, friendData.profile_img, friendData.status_msg, () => {
                        const infoFriendModal = new InfoFriendModal();
                        this.el.appendChild(infoFriendModal.el);
                        infoFriendModal.open();
                    });

                    this.el.querySelector('.friends').appendChild(friend.el);
                });
            } catch (error) {
                // console.error('친구 목록을 가져오는 중 오류 발생:', error);
            }
        };

        fetchFriends();
    }
    render() { }
}
