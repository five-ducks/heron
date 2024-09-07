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

		// 초기화
		this.selectCharactor(this.charactors[0]); // 초기 선택된 캐릭터
		this.selectedIndex = 0; // 초기 선택된 캐릭터 인덱스

		this.charactors.forEach(charactor => {
			this.el.appendChild(charactor.el);
		});
	}

	// 캐릭터 선택 메서드
	selectCharactor(selectedCharactor) {
		if (this.selectedCharactor) {
			this.selectedCharactor.deselect(); // 이전 선택된 캐릭터 선택 해제
		}

		this.selectedCharactor = selectedCharactor;
		this.selectedCharactor.select(); // 새로 선택된 캐릭터 선택

		// 선택된 캐릭터의 인덱스를 찾아 커스텀 이벤트를 생성하여 발생시킴
		const selectedIndex = this.charactors.indexOf(selectedCharactor);
		const event = new CustomEvent('charactorSelected', { detail: { index: selectedIndex } });
		this.el.dispatchEvent(event); // 이벤트 발생
	}

	render() {
	}
}
