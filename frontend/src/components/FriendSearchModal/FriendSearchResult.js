import { getCookie } from "../../core/core.js";
import { Profile } from "../Profile/Profile.js";

export class FriendSearchResult {
    constructor(friend) {
        this.friend = friend;
        this.el = document.createElement('div');
        this.el.className = 'friend-search-result';
    }

    render() {
        const friendProfile = new Profile(
            this.friend.profile_img,
            this.friend.username,
            'm',
            {
                status_msg: this.friend.status_msg,
                onSelect: () => {}
            }
        );
    
        // 친구 추가 버튼 생성
        const addButton = document.createElement('button');
        addButton.className = 'add-friend-btn';
        addButton.textContent = '친구 추가';
        addButton.addEventListener('click', () => this.addFriend());
    
        // 컴포넌트에 요소들 추가
        const searchResultsContainer = document.getElementById('search-results');
        searchResultsContainer.appendChild(friendProfile.el);
        searchResultsContainer.appendChild(addButton);
    }

    async addFriend() {
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
        this.updateButtonState();
    }
    
    updateButtonState() {
        const addButton = document.querySelector('.add-friend-btn');
        addButton.textContent = '추가됨';
        addButton.disabled = true;
        addButton.classList.add('added');
    }
}