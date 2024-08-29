import { Component } from "../core/core.js";
import { Header } from "../components/Header/Header.js";
import { MyProfileContent } from "../components/MyProfileContent/MyProfileContent.js";

export default class MyProfile extends Component {
	render() {
		this.el.innerHTML = /*html*/`
		<div class="headerpos"></div>
		<div class="my-profile"></div>
		`;
		this.el.querySelector('.headerpos').appendChild(new Header().el);
		this.el.querySelector('.my-profile').appendChild(new MyProfileContent().el);

	}
}