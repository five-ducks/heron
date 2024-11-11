import { Component } from "../core/core.js";
import { Header } from "../components/Header/Header.js";
import { SelectPage } from "../components/SelectPage/SelectPage.js";
import { Sidebar } from "../components/Sidebar/Sidebar.js";
import gameStore, { loadUserInfo } from "../store/game.js";
import { startWebSocketConnection } from '../status/status.js';

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
            <div class="contents">
                <div class="game-section"></div>
                <aside class="sidebar"></aside>
            </div>
        `
        await loadUserInfo();
        startWebSocketConnection();
        const header = new Header(gameStore.state.userInfo);
        this.el.querySelector('.headerpos').appendChild(header.el);

        const selectpage = new SelectPage();
        this.el.querySelector('.game-section').appendChild(selectpage.el);

        const sidebar = new Sidebar(gameStore.state.userInfo);
        this.el.querySelector('.sidebar').appendChild(sidebar.el);
    }
}