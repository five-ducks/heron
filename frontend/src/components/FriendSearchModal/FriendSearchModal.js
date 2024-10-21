import { Modal } from "../Modal/index.js";
import { FriendSearchResult } from "./FriendSearchResult.js";

export class FriendSearchModal extends Modal {
    constructor() {
        super(FriendSearchModal.getContent(), () => this.onModalClose());
        this.searchInput = this.el.querySelector('#friend-search-input');
        this.searchResults = this.el.querySelector('#search-results');
        this.searchButton = this.el.querySelector('#search-button');

        this.searchButton.addEventListener('click', () => this.performSearch());
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch();
            }
        });
    }

    static getContent() {
        return /*html*/`
            <h2>친구 검색</h2>
            <input type="text" id="friend-search-input" placeholder="친구 이름을 입력하세요">
            <button id="search-button">검색</button>
            <div id="search-results"></div>
        `;
    }

    async performSearch() {
        // 입력된 검색어 가져오기
        const searchTerm = this.searchInput.value.trim();

        // API 호출
        try {
            const response = await fetch(`api/users/?search=${searchTerm}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (response.status === 200) {
                const friendList = await response.json();

                // 검색 결과 초기화
                this.searchResults.innerHTML = '';

                // 검색 결과가 없는 경우 메시지 표시
                if (friendList.length === 0) {
                    this.searchResults.innerHTML = '<p>검색 결과가 없습니다.</p>';
                    return;
                }

                // 검색 결과 표시
                friendList.forEach(friend => {
                    const friendResult = new FriendSearchResult(friend);
                    friendResult.render();
                });
            }
            if (response.status === 404) {
                this.searchResults.innerHTML = '<p>검색 결과가 없습니다.</p>';
            }
        } catch (error) {
            console.error('검색 중 오류 발생:', error);
            this.searchResults.innerHTML = '<p>검색 중 오류가 발생했습니다. 다시 시도해주세요.</p>';
        }
    }

    onModalClose() {
        // 모달이 닫힐 때 수행할 작업
        this.searchInput.value = '';
        this.searchResults.innerHTML = '';
    }
}