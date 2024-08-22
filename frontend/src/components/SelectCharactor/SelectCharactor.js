import { Component } from "../../core/core.js";
import { Charactor } from "./Charactor.js";

export class SelectCharactor extends Component {
	constructor() {
		super({
			tagName: 'div',
			props: {
				className: 'select-charactor'
			}
		});

		this.selectedCharactor = null;

		this.charactors = [
			new Charactor({ src: '../public/images/charactors/pikachu.png'}, '피카츄', this.selectCharactor.bind(this)),
			new Charactor({ src: '../public/images/charactors/charmander.png' }, '파이리', this.selectCharactor.bind(this)),
			new Charactor({ src: '../public/images/charactors/bulbasaur.png' }, '이상해씨', this.selectCharactor.bind(this)),
			new Charactor({ src: '../public/images/charactors/squirtle.png' }, '꼬부기', this.selectCharactor.bind(this)),
			new Charactor({ src: '../public/images/charactors/eevee.png' }, '이브이', this.selectCharactor.bind(this)),
			new Charactor({ src: '../public/images/charactors/snorlax.png' }, '잠만보', this.selectCharactor.bind(this)),
			new Charactor({ src: '../public/images/charactors/mew.png' }, '뮤', this.selectCharactor.bind(this)),
			new Charactor({ src: '../public/images/charactors/ditto.png' }, '메타몽', this.selectCharactor.bind(this)),
		];

		this.selectCharactor(this.charactors[0]);
		console.log(this.charactors);

		this.charactors.forEach(charactor => {
			this.el.appendChild(charactor.el);
		});
	}

	selectCharactor(selectedCharactor) {
		if (this.selectedCharactor) {
			this.selectedCharactor.deselect();
		}

		this.selectedCharactor = selectedCharactor;
		this.selectedCharactor.select();
	}

	render() {
	}
}
