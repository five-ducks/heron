import { Component } from "../../core/core.js";
import { InfoFriendModal } from "../InfoFriendModal/InfoFriendModal.js";
import { FriendSearchModal } from "../FriendSearchModal/FriendSearchModal.js";
import { Button } from "../Button.js";
import { Profile } from "../Profile/Profile.js";
import { getCookie } from "../../core/core.js";
import store from "../../store/game.js";

export class Sidebar extends Component {
    constructor() {
        super({
            tagName: 'div',
            props: {
                className: 'friendwindow'
            },
        });
        this.friendRender();
        store.subscribe('userFriends', this.renderFriendList.bind(this));
    }

    friendRender() {
        this.el.classList.add('container'); // Bootstrap container 클래스 추가
        this.el.classList.add('col-auto'); // col-auto로 설정하여 내용물에 맞게 크기 조절

        this.el.innerHTML = /*html*/`
            <div class="addfriend text-center mb-3"></div>
            <div class="friends list-group"></div>
        `;

        // 친구 추가 버튼
        const addFriendButton = new Button(
            {
                style: 'sidebar',
                size: 'md',
                text: '친구 추가 +'
            },
            () => {
                const friendSearchModal = new FriendSearchModal();
                this.el.appendChild(friendSearchModal.el);
                friendSearchModal.open();
            }
        );
        this.el.querySelector('.addfriend').appendChild(addFriendButton.el);

        // 친구 목록 가져오기
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
                if (response.ok) {
                    store.state.userFriends = friendsInfo;
                } else {
                    console.error('친구 목록을 가져오는 중 오류 발생:', friendsInfo.error);
                    store.state.userFriends = [];
                }

                // 가져온 친구 목록을 Store의 userFriends 상태에 저장합니다.

            } catch (error) {
                console.error('친구 목록을 가져오는 중 오류 발생:', error);
            }
        };
        fetchFriends();
    }

    renderFriendList() {
        const friendsContainer = this.el.querySelector('.friends');
        friendsContainer.innerHTML = ''; // 기존 친구 목록을 지움

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
                    },
                    status: friendData.status,
                },
            );
            // 각 친구 항목을 리스트 그룹 아이템으로 추가
            const friendItem = document.createElement('div');
            friendItem.classList.add('list-group-item'); // Bootstrap 리스트 그룹 아이템 클래스 추가
            friendItem.appendChild(friend.el);
            friendsContainer.appendChild(friendItem);
            const deleteButton = new Button(
                {
                    style: 'gray',
                    size: 'sm',
                    text: 'X'
                },
                async () => {
                    const deleteUrl = `/api/users/self/friends/?friendname=${friendData.username}`;
                    try {
                        const response = await fetch(deleteUrl, {
                            method: 'DELETE',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCookie('csrftoken'),
                            },
                        });
                        if (response.ok) {
                            console.log('친구 삭제에 성공했습니다');
                            friendItem.remove();
                        } else {
                            console.error('친구 삭제 중 오류 발생:', response.error);
                        }
                    } catch (error) {
                        console.error('친구 삭제 중 오류 발생:', error);
                    }
                }
            );
            deleteButton.el.classList.add('delete-button');
            friend.el.appendChild(deleteButton.el);
        });
    }

    render() { }
}
