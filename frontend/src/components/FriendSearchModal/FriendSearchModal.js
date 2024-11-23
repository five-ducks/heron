import { Modal } from "../Modal/index.js";
import { FriendSearchResult } from "./FriendSearchResult.js";
import { Button } from "../Button.js";
import { Input } from "../Input/Input.js";
import { quickAlert } from "../Alert/Alert.js";

export class FriendSearchModal extends Modal {
    constructor() {
        super('친구 검색', FriendSearchModal.getContent(), () => this.onModalClose());
        this.searchResults = this.el.querySelector('.search-results');
        this.searchContainer = this.el.querySelector('.search-container');
        
        this.searchInput = new Input({
            placeholder: '친구 이름 입력',
            type: 'text',
            size: 'l',
        });
        this.searchButton = new Button({ style: 'gray', size: 'lg', text: '검색' }, async () => await this.performSearch());
        this.searchInput.el.classList.add('col-9');
        this.searchButton.el.classList.add('col-3');
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
            <div class="row search-container"></div>
            <div class="search-results"></div>
        `;
    }

    async performSearch() {
        try {
            const searchTerm = this.searchInput.getValue();
            const response = await fetch(`api/users/?search=${searchTerm}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            this.searchResults.innerHTML = '';
            if (response.ok) {
                const friendList = await response.json();
                friendList.forEach(friend => {
                    const friendResult = new FriendSearchResult(friend);
                    this.searchResults.appendChild(friendResult.el);
                    friendResult.friendProfileRender();
                });
            } else if (response.status === 404) {
                await quickAlert('검색 결과가 없습니다.');
            } else {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        } catch (error) {
            await quickAlert(`친구 검색 중 에러: ${error.message}`);
        }
    }

    onModalClose() {
        this.searchInput.setValue('');
        this.searchResults.innerHTML = '';
    }
}