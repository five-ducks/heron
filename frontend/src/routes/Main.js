import { Component } from "../core/core.js";
import { Header } from "../components/Header/Header.js";
import { SelectPage } from "../components/SelectPage/SelectPage.js";
import { Sidebar } from "../components/Sidebar/Sidebar.js";
import { MyProfileContent } from "../components/MyProfileContent/MyProfileContent.js";
import gameStore, { loadUserInfo } from "../store/game.js";

export default class Main extends Component {
    constructor() {
        super({
            props: {
                className: 'main',
            }
        });
        this.currentView = gameStore.state.currentView;
    }

    async render() {
        this.el.innerHTML = /*html*/`
            <div class="head-line row flex-column flex-xxl-row"></div>
            <div class="body-line row">
                <div class="main-content col-xxl-9"></div>
                <div class="sidebar-container col-xxl-3"></div>
            </div>
        `;
        await loadUserInfo();
        const header = new Header(gameStore.state.userInfo, this.switchView.bind(this));
        this.el.querySelector('.head-line').appendChild(header.el);

        // Sidebar 컴포넌트 추가 (항상 표시)
        const sidebar = new Sidebar();
        this.el.querySelector('.sidebar-container').appendChild(sidebar.el);

        // 초기 뷰 렌더링
        this.renderCurrentView();
    }

    switchView() {
        this.currentView = this.currentView === 'selectPage' ? 'myProfile' : 'selectPage';
        this.renderCurrentView();
    }

    renderCurrentView() {
        const mainContent = this.el.querySelector('.main-content');
        mainContent.innerHTML = '';
        
        if (this.currentView === 'selectPage') {
            const selectPage = new SelectPage();
            mainContent.appendChild(selectPage.el);
        } else if (this.currentView === 'myProfile') {
            const myProfileContent = new MyProfileContent();
            mainContent.appendChild(myProfileContent.el);
        }
        localStorage.setItem('currentView', this.currentView);
    }
}