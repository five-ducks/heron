import { Component } from "../../core/core.js";
import { FriendProfile } from "../Profile/FriendProfile.js";
import { InfoFriendModal } from "../InfoFriendModal/InfoFriendModal.js";
import { getCookie } from "../../core/core.js";

export class Sidebar extends Component {
    render() {
        this.el.classList.add('friendwindow');
        this.el.innerHTML = /*html*/`
            <button class="addfriend">친구추가 +</button>
            <div class="friends"></div>
        `;

        const fetchFriends = async () => {
            // 쿠키에서 player 값을 가져옵니다.
            const player = getCookie('player'); // 'player'가 쿠키 이름이라고 가정합니다.
            const allUrl = `/api/users/self/friends`;

            try {
                const response = await fetch(allUrl, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                });
                console.log('response:', response);
                const friendsInfo = await response.json();

                // 가져온 친구 목록을 반복하면서 FriendProfile 컴포넌트를 생성합니다.
                friendsInfo.forEach(friendData => {
                    const friend = new FriendProfile(friendData.username, friendData.img, friendData.status_msg, () => {
                        const infoFriendModal = new InfoFriendModal();
                        this.el.appendChild(infoFriendModal.el);
                        infoFriendModal.open();
                    });

                    this.el.querySelector('.friends').appendChild(friend.el);
                });
            } catch (error) {
                console.error('친구 목록을 가져오는 중 오류 발생:', error);
            }
        };

        fetchFriends();
    }
}
