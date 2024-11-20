import { Component } from "./core/core.js"

export default class App extends Component {
	render() {
		const routerView = document.createElement('router-view');
		routerView.classList.add('router-view');
		this.el.append(routerView);
	}
}