import { Component } from "../core/core.js";
import { Header } from "../components/Header/Header.js";
import { SelectPage } from "../components/SelectPage/SelectPage.js";
import { Sidebar } from "../components/Sidebar/Sidebar.js";

export default class Main extends Component {
    render(){
        this.el.classList.add('main');

		this.el.innerHTML = /*html*/`
            <div class="headerpos"></div>
            <div class="body">
                <div class="selectpage"></div>
                <div class="sidebar"></div>
            </div>
        `
        const header = new Header();
        this.el.querySelector('.headerpos').appendChild(header.el);

        const selectpage = new SelectPage();
        this.el.querySelector('.selectpage').appendChild(selectpage.el);

        const sidebar = new Sidebar();
        this.el.querySelector('.sidebar').appendChild(sidebar.el);
    }
}