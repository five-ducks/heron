import { Component } from "../../core/core.js";
import { FriendProfile } from "../Profile/FriendProfile.js";
import { InfoFriendModal } from "../InfoFriendModal/InfoFriendModal.js";
import { FriendSearchModal } from "../FriendSearchModal/FriendSearchModal.js";
import { Button } from "../Button.js";
import { Profile } from "../Profile/Charactor.js";
import store from "../../store/game.js"; // Store 불러오기

export class Sidebar extends Component {
    constructor(props) {
        super();
        this.userInfo = props;

        // 친구 목록을 불러오기 위해 fetchFriends 함수를 호출합니다.
        this.friendRender(this.userInfo);

        // Store에 친구 목록이 업데이트될 때 마다 renderFriendList를 호출합니다.
        store.subscribe('userFriends', this.renderFriendList.bind(this));
    }

    friendRender(userInfo) {
        this.el.classList.add('friendwindow');
        this.el.innerHTML = /*html*/`
            <div class="addfriend"></div>
            <div class="friends"></div>
        `;

        // 이미지 수정 필요 
        const addFriendButton = new Button(
            {
                width: '200px',
                height: '50px',
                background: "url('../public/images/button.png')",
                color: 'white',
                size: '16px'
            },
            '친구추가 +',
            () => {
                const friendSearchModal = new FriendSearchModal();
                this.el.appendChild(friendSearchModal.el);
                friendSearchModal.open();
            }
        );
        this.el.querySelector('.addfriend').appendChild(addFriendButton.el);

        const fetchFriends = async () => {
            const allUrl = `/api/users/self/friends/`;
            try {
                const response = await fetch(allUrl, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                });
                const friendsInfo = await response.json();

                // 가져온 친구 목록을 Store의 userFriends 상태에 저장합니다.
                store.state.userFriends = friendsInfo;

            } catch (error) {
                console.error('친구 목록을 가져오는 중 오류 발생:', error);
            }
        };
        fetchFriends();
    }

    renderFriendList() {
        const friendsContainer = this.el.querySelector('.friends');
        friendsContainer.innerHTML = ''; // Clear existing friend list
    
        // Use store.state.userFriends to create FriendProfile components
        store.state.userFriends.forEach(friendData => {
            const friend = new Profile(
                friendData.profile_img,
                friendData.username,
                'm',
                {
                    status_msg: friendData.status_msg,
                    onSelect: () => {
                        const infoFriendModal = new InfoFriendModal(friendData);
                        this.el.appendChild(infoFriendModal.el);
                        infoFriendModal.open();
                    }
                }
            );
            friendsContainer.appendChild(friend.el);
        });
    }

    render() { }
}
