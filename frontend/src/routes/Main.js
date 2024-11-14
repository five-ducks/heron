import { Component } from "../core/core.js";
import { Header } from "../components/Header/Header.js";
import { SelectPage } from "../components/SelectPage/SelectPage.js";
import { Sidebar } from "../components/Sidebar/Sidebar.js";
import gameStore, { loadUserInfo } from "../store/game.js";
import { startWebSocketConnection } from "../status/status.js";

export default class Main extends Component {
    constructor() {
        super({
            props: {
                className: 'main',
            }
        });
    }

    async render() {
        this.el.innerHTML = /*html*/`
            <header class="headerpos"></header>
            <div class="container-fluid">
                <div class="row contents d-flex flex-column flex-xxl-row">
                    <div class="col-12 col-xxl-9 game-section-container">
                        <!-- SelectPage가 여기에 추가됩니다 -->
                    </div>
                    <aside class="col-12 col-xxl-3 sidebar-container">
                        <!-- Sidebar가 여기에 추가됩니다 -->
                    </aside>
                </div>
            </div>
        `
        await loadUserInfo();
        startWebSocketConnection();

        // Header 컴포넌트 추가
        const header = new Header(gameStore.state.userInfo);
        this.el.querySelector('.headerpos').appendChild(header.el);

        // SelectPage 컴포넌트 추가
        const selectpage = new SelectPage();
        this.el.querySelector('.game-section-container').appendChild(selectpage.el);

        // Sidebar 컴포넌트 추가
        const sidebar = new Sidebar(gameStore.state.userInfo);
        this.el.querySelector('.sidebar-container').appendChild(sidebar.el);
    }
}
