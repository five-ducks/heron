import { FriendProfile } from "../Profile/FriendProfile.js";
import { getCookie } from "../../core/core.js";

export class FriendSearchResult {
    constructor(friend) {
        this.friend = friend;
        this.el = document.createElement('div');
        this.el.className = 'friend-search-result';
    }

    render() {
        // FriendProfile 컴포넌트 생성
        const friendProfile = new FriendProfile(
            this.friend.username,
            this.friend.profile_img,
            this.friend.status_msg,
            () => {} // 클릭 이벤트는 여기서는 비워둡니다
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
