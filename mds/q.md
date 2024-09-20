### /Users/seokjyan/Desktop/tcen/frontend/src/components/GameRecords/GameRecords.css
```.css
.game-records {
	display: flex;
    gap: 10px;
    flex-direction: column;
}
```

### /Users/seokjyan/Desktop/tcen/frontend/src/components/GameRecords/GameRecords.js
```.js
import { Component } from "../../core/core.js";
import { OneGameRecord } from "./OneGameRecord.js";
import store, { loadGameRecords } from "../../store/game.js"; 

// 전적 영역
export class GameRecords extends Component {
	constructor() {
		super({
			props: {
				className: 'game-records',
			}
		});
	}

	async render() {
		await loadGameRecords();

		this.el.innerHTML = /*html*/``;

		const gameRecords = store.state.gameRecords.gameRecords;
		if (gameRecords) {
			gameRecords.forEach(gameRecord => {
				const oneGameRecord = new OneGameRecord();
				oneGameRecord.render(gameRecord);
				this.el.appendChild(oneGameRecord.el);
			});
		}
	}
}

```

### /Users/seokjyan/Desktop/tcen/frontend/src/components/GameRecords/OneGameRecord.css
```.css
.one-game-record {
	display: flex;
	width: 600px;
	height: 95px;
	padding: 10px;
	font-family: 'DungGeunMo';
	background-size: cover;
}

.one-game-record .game-type {
	display: flex;
    min-width: 75px;
    align-items: center;
    font-size: 15px;
    flex-direction: column;
    justify-content: center;
}

.one-game-record .vs-text {
	display: flex;
	font-size: 50px;
	align-items: center;
	justify-content: center;
	padding: 5px 5px 5px 15px;
}

.one-game-record .match-time {
	display: flex;
	align-items: center;
	justify-content: center;
	margin-left: 15px;
}
```

### /Users/seokjyan/Desktop/tcen/frontend/src/components/GameRecords/OneGameRecord.js
```.js
import { Component } from "../../core/core.js";
import store from "../../store/game.js";
import { Outcome } from "./Outcome.js";

// 하나의 게임 결과
export class OneGameRecord extends Component {
	constructor() {
		super({
			props: {
				className: 'one-game-record',
			}
		});
	}
	render(gameRecord) {
		const myName = "Ava"; // 내 아이디 (임시)
		if (gameRecord) {
			const user1_name = gameRecord.user1_name;
			const user2_name = gameRecord.user2_name;
			const match_result = gameRecord.match_result;
			const match_time = new Date(gameRecord.match_end_time);
			const user1IsWin = ( match_result === 'user1_win');
			const user2IsWin = ( match_result === 'user2_win');
			let isWin; // 내가 이겼는지 졌는지
			if (user1_name === myName) {
				isWin = user1IsWin;
			}
			if (user2_name === myName) {
				isWin = user2IsWin;
			}

			// 날짜와 시간 포맷 지정
			const year = match_time.getFullYear();
			const month = String(match_time.getMonth() + 1).padStart(2, '0'); // 월은 0부터 시작하므로 +1 필요
			const day = String(match_time.getDate()).padStart(2, '0');
			const hours = String(match_time.getHours()).padStart(2, '0');
			const minutes = String(match_time.getMinutes()).padStart(2, '0');

			// 형식에 맞게 날짜와 시간 결합
			const formattedDateTime = `${year}/${month}/${day}<br>${hours}:${minutes}`;
			let match_type = 'single';

			if (gameRecord.match_type === 'single') {
				match_type = '1 : 1';
			} else {
				match_type = '토너먼트';
			}

			this.el.innerHTML = /*html*/`
				<div class="game-type">${match_type}</div>
				<div class="left-user"></div>
				<div class="vs-text">VS</div>
				<div class="right-user"></div>
				<div class="match-time">${formattedDateTime}</div>
			`

			const leftUSer = this.el.querySelector('.left-user');
			const rightUser = this.el.querySelector('.right-user');
			const leftOutcome = new Outcome();
			const rightOutcome = new Outcome();
			leftOutcome.render(user1IsWin, user1_name);
			rightOutcome.render(user2IsWin, user2_name);
			leftUSer.appendChild(leftOutcome.el);
			rightUser.appendChild(rightOutcome.el);

			if (isWin) {
				this.el.style.backgroundImage = "url('../../../public/images/win-bg.png')";
			} else {
				this.el.style.backgroundImage = "url('../../../public/images/lose-bg.png')";
			}
		}
	}
}

```

### /Users/seokjyan/Desktop/tcen/frontend/src/components/GameRecords/Outcome.css
```.css
.game-records .one-game-record .outcome {
	display: flex;
	height: 75px;
	align-items: center;
	font-family: 'DungGeunMo';
}

.game-records .one-game-record .profile-container {
	display: flex;
    position: relative;
    top: 15%;
    width: 85px;
    height: 75px;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}


.game-records .one-game-record .profile-container .profile-result-img {
	min-width: 50px;
    min-height: 50px;
    background-color: #dee2e6;
    border-radius: 50%;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}

.game-records .one-game-record .profile-container .profile-result-img img {
	width: 100%;
	height: 100%;
	object-fit: cover;
	margin-left: 5px;
	justify-content: center;
    align-items: center;
}

.game-records .one-game-record .profile-container .user-name {
	position: relative;
	font-size: 20px;
	top: -20px;
	margin-top: 0px;
	text-shadow: 
        -1px -1px 0 black,
        1px -1px 0 black,
        -1px  1px 0 black,
        1px  1px 0 black;
}

.game-records .one-game-record .result {
	display: flex;
	align-items: center;
	justify-content: center;
	min-width: 65px;
	font-size: 30px;
}
```

### /Users/seokjyan/Desktop/tcen/frontend/src/components/GameRecords/Outcome.js
```.js
import { Component } from "../../core/core.js";

export class Outcome extends Component {
	constructor() {
		super({
			props: {
				className: 'outcome',
			}
		});
	}
	render(isWin, userName) {

		const result = isWin ? 'WIN' : 'LOSE';
		
		this.el.innerHTML = /*html*/`
			<div class="profile-container">
				<div class="profile-result-img"></div>
				<div class="user-name">${userName}</div>
			</div>
			<div class="result">
				${result}
			</div>
		`
		const profileImg = this.el.querySelector('.profile-result-img'); 
		const img = document.createElement('img');
		img.src = '../../../public/images/charactors/pikachu.png';
		// 여기 userId로 이미지 찾는거 넣어야함
		// 지금은 임시 이미지
		profileImg.appendChild(img);

		const resultEl = this.el.querySelector('.result');

		// 이겼으면 파란색, 졌으면 빨간색 텍스트 테두리를 설정
		if (isWin) {
            resultEl.style.textShadow = '-1px 1px 0px #0000ff, 1px -1px 0px #0000ff, -1px -1px 0px #0000ff, 1px 1px 0px #0000ff';
        } else {
            resultEl.style.textShadow = '-1px 1px 0px #ff0000, 1px -1px 0px #ff0000, -1px -1px 0px #ff0000, 1px 1px 0px #ff0000'; ;
        }

	}
}
```

