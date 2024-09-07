import { Component } from "../core/core.js";
import { Header } from "../components/Header/Header.js";
import { MyProfileContent } from "../components/MyProfileContent/MyProfileContent.js";
import { Sidebar } from "../components/Sidebar/Sidebar.js";

export default class MyProfile extends Component {
	render() {
		this.el.innerHTML = /*html*/`
		<div class="headerpos"></div>
		<div class="body">
			<div class="my-profile"></div>
			<div class="sidebar"></div>
		</div>
		`;
		this.el.querySelector('.headerpos').appendChild(new Header().el);
		this.el.querySelector('.my-profile').appendChild(new MyProfileContent().el);
		this.el.querySelector('.sidebar').appendChild(new Sidebar().el);

	}
}
