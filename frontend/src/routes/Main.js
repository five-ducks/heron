import { Component } from "../core/core.js";
import { Header } from "../components/Header/Header.js";
import { SelectPage } from "../components/SelectPage/SelectPage.js";
import { Sidebar } from "../components/Sidebar/Sidebar.js";
import gameStore, { loadUserInfo } from "../store/game.js";

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
            <div class="head-line row flex-column flex-xxl-row"></div>
            <div class="body-line row"></div>
        `;
        await loadUserInfo();
        const header = new Header(gameStore.state.userInfo);
        this.el.querySelector('.head-line').appendChild(header.el);

        // SelectPage 컴포넌트 추가
        const selectpage = new SelectPage();
        selectpage.el.classList.add('col-xxl-9');
        this.el.querySelector('.body-line').appendChild(selectpage.el);

        // Sidebar 컴포넌트 추가
        const sidebar = new Sidebar();
        sidebar.el.classList.add('col-xxl-3');
        this.el.querySelector('.body-line').appendChild(sidebar.el);
    }
}
