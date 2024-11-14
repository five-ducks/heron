import { Modal } from "../Modal/index.js";
import { FriendSearchResult } from "./FriendSearchResult.js";
import { Button } from "../Button.js";
import { Input } from "../Input/Input.js";

export class FriendSearchModal extends Modal {
    constructor() {
        super('친구 검색', FriendSearchModal.getContent(), () => this.onModalClose());
        this.searchResults = this.el.querySelector('.search-results');
        this.searchContainer = this.el.querySelector('.search-container');

        this.searchInput = new Input('친구 이름 입력', 'text', { width: '330px', height: '65px', fontsize: '20px' }, '', '', 'friend-search-input');
        // this.searchButton = new Button({ style: 'gray', size: 's', text: '검색' }, () => this.performSearch());
        this.searchButton = new Button({ style: 'gray', size: 'lg', text: '검색' }, async () => await this.performSearch());
        this.searchContainer.appendChild(this.searchInput.el);
        this.searchContainer.appendChild(this.searchButton.el);

        this.searchInput.el.querySelector('input').addEventListener('keypress', async (e) => {
            if (e.key === 'Enter') {
                await this.performSearch();
            }
        });
    }

    static getContent() {
        return /*html*/`
            <div class="search-container"></div>
            <div class="search-results"></div>
        `;
    }

    async performSearch() {
        const searchTerm = this.searchInput.getValue();

        try {
            const response = await fetch(`api/users/?search=${searchTerm}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            this.searchResults.innerHTML = '';

            if (response.ok) {
                const friendList = await response.json();

                if (friendList.length === 0) {
                    this.searchResults.innerHTML = '<p>친구를 찾을 수 없음.</p>';
                    return;
                }

                friendList.forEach(friend => {
                    const friendResult = new FriendSearchResult(friend);
                    this.searchResults.appendChild(friendResult.el);
                    friendResult.friendProfileRender();
                });
            } else if (response.status === 404) {
                this.searchResults.innerHTML = '<p>결과 없음.</p>';
            } else {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        } catch (error) {
            console.error('에러:', error);
            this.searchResults.innerHTML = '<p>에러</p>';
        }
    }

    onModalClose() {
        this.searchInput.setValue('');
        this.searchResults.innerHTML = '';
    }
}