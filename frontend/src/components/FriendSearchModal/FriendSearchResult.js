import { Component } from "../../core/core.js";
import { Profile } from "../Profile/Profile.js";
import { getCookie } from "../../core/core.js";
import { Button } from "../Button.js";
import store from "../../store/game.js";

export class FriendSearchResult extends Component {
    constructor(friend) {
        super({
            tagName: 'div',
            props: {
                className: 'friend-search-result',
            }
        });
        this.friend = friend;
        this.addButton = null;
        console.log(friend);
        console.log(store.state.userFriends);
        console.log(store.state.userFriends.some(f => f.username === this.friend.username));
        this.isFriend = store.state.userFriends.some(f => f.username === this.friend.username);
    }

    friendProfileRender() {
        const friendProfile = new Profile(
            this.friend.profile_img,
            this.friend.username,
            'm',
            {
                status_msg: this.friend.status_msg,
                onSelect: () => { }
            }
        );
        friendProfile.el.classList.add('friend-profile');

        const bt = this.isFriend ? '추가됨' : '친구 +';

        this.addButton = new Button({
            style: 'gray',
            size: 's',
            text: bt
        }, () => this.addFriend());
        this.addButton.el.classList.add('add-friend-btn');

        // 컴포넌트에 요소들 추가
        this.el.appendChild(friendProfile.el);
        this.el.appendChild(this.addButton.el);
    }

    async addFriend() {
        try {
            const response = await fetch(`api/users/self/friends/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    friendname: this.friend.username,
                }),
            });

            if (response.ok) {
                this.updateButtonState();
            } else {
                console.error('친구 추가 에러:', await response.text());
            }
        } catch (error) {
            console.error('친구 추가 에러:', error);
        }
    }

    updateButtonState() {
        if (this.addButton) {
            this.addButton.setText('추가됨');
            this.addButton.el.disabled = true;
            this.addButton.el.classList.add('added');
        } else {
            console.error('버튼이 없습니다.');
        }
    }
}