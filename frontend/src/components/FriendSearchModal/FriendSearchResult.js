export class FriendSearchResult {
    constructor(friend) {
        this.friend = friend;
        this.element = this.createResultElement();
    }

    createResultElement() {
        const resultElement = document.createElement('div');
        resultElement.className = 'friend-search-result';
        resultElement.innerHTML = `
            <img src="/assets/profile-images/${this.friend.profile_img}.png" alt="${this.friend.username}'s profile" class="profile-img">
            <div class="friend-info">
                <h3>${this.friend.username}</h3>
                <p>${this.friend.status_msg}</p>
            </div>
            <button class="${this.friend.is_friend ? 'remove-friend' : 'add-friend'}">
                ${this.friend.is_friend ? '친구 삭제' : '친구 추가'}
            </button>
        `;

        const button = resultElement.querySelector('button');
        button.addEventListener('click', () => this.toggleFriendship());

        return resultElement;
    }

    toggleFriendship() {
        // 여기에 친구 추가 API 호출 로직을 구현합니다.
        // API 호출이 성공하면 버튼의 텍스트와 클래스를 변경합니다.
        const button = this.element.querySelector('button');
        if (this.friend.is_friend) {
            // 친구 삭제 API 호출 로직
        }
    }
}