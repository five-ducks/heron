import { Component } from "../../core/core.js";

export class MatchRecord extends Component {
    render() {
        this.el.classList.add("match_record");
        this.el.innerHTML = /*html*/`
            <div class="type"></div>
            <div class="my_profile"></div>
            <div class="vs"></div>
            <div class="friend_profile"></div>
            <div class="result"></div>
            <div class="date"></div
        `
    }
}