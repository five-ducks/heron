// import { Component } from "../core/core"
// import Header from "../components/Header"
// import MainBoard from "../components/MainBoard"
// import SideBar from "../components/SideBar"

// expeort default class Lobby extends Component {
// 	render() {
// 		this.el.innerHTML = /*html*/`
// 		<div class="lobby">
// 			<header></header>
// 			<main></main>
// 			<aside></aside>
// 		</div>
// 		`
// 		this.el.querySelector('header').append(new Header().el)
// 		this.el.querySelector('main').append(new MainBoard().el)
// 		this.el.querySelector('aside').append(new SideBar().el)
// 		const style = document.createElement('style')
// 		style.textContent = /*css*/`
// 			.lobby {
// 				display: grid;
// 				grid-template-columns: 1fr 3fr 1fr;
// 				height: 100vh;
// 			}
// 		`
// 		this.el.appendChild(style)
// 	}
// }