import { Component } from "../../core/core.js";
import { ProfileIcon } from "../Profile/ProfileIcon.js";

export class MatchRecord extends Component {
    // MatchInfo를 받음
    constructor ( matchInfo = {} ) {
        super();
        this.el.innerHTML = /*html*/`
            <div class="type"></div>
            <div class="myProfileIcon"></div>
            <div class="vs"></div>
            <div class="friendProfileIcon"></div>
            <div class="result"></div>
            <div class="date"></div>
        `
        this.el.classList.add('match-record');
        this.el.querySelector('.type').textContent = '1:1';
        this.el.querySelector('.vs').textContent = 'VS';
        this.el.querySelector('.result').textContent = '승리';
        this.el.querySelector('.date').textContent = '2021-07-01';

        const myProfileIcon = new ProfileIcon();
        const friendProfileIcon = new ProfileIcon();
        this.el.querySelector('.myProfileIcon').appendChild(myProfileIcon.el);
        this.el.querySelector('.friendProfileIcon').appendChild(friendProfileIcon.el);

        this.render();
    }
    render() {
    }
}