import { Component } from "../core/core.js";
import { Header } from "../components/Header/Header.js";
import { SelectPage } from "../components/SelectPage/SelectPage.js";
import { Sidebar } from "../components/Sidebar/Sidebar.js";
import gameStore, { loadUserInfo } from "../store/game.js";

export default class Main extends Component {
    async render() {
        this.el.classList.add('main');

        this.el.innerHTML = /*html*/`
            <header class="headerpos"></header>
            <div class="body">
                <div class="selectpagepos"></div>
                <aside class="sidebar"></aside>
            </div>
        `
        await loadUserInfo();
        const header = new Header(gameStore.state.userInfo);
        this.el.querySelector('.headerpos').appendChild(header.el);

        const selectpage = new SelectPage();
        this.el.querySelector('.selectpagepos').appendChild(selectpage.el);

        const sidebar = new Sidebar(gameStore.state.userInfo);
        this.el.querySelector('.sidebar').appendChild(sidebar.el);
    }
}