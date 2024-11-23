import { startWebSocketConnection, getSocketStatus } from '../status/status.js';

///// Component /////
export class Component {
	constructor(payload = {}) {
		const {
			tagName = 'div', // 최상위 요소의 태그 이름
			props = {},
			state = {},
			style = {},
		} = payload
		this.el = document.createElement(tagName) // 컴포넌트의 최상위 요소
		if (props.className) {
			this.el.className = props.className;
		}
		this.state = state // 컴포넌트 안에서 사용할 데이터
		this.render()
	}
	render() { // 컴포넌트를 렌더링하는 함수
		// ...
	}
}

// cookie가 있는지 조회하는 함수
export function getCookie(name) {
	const value = `; ${document.cookie}`;			// 쿠키 값 앞에 ;를 붙여서 쿠키 이름을 찾을 때 편리하게 함
	const parts = value.split(`; ${name}=`);		// 쿠키 이름을 기준으로 쿠키 값을 분리
	if (parts.length === 2)							// 쿠키 값이 존재한다면
		return parts.pop().split(';').shift();		// 쿠키 값을 반환
	return null;									// 쿠키 값이 존재하지 않는다면 null을 반환
}

async function routeRender(routes) {
	if (!location.hash) {
		history.replaceState(null, '', '/#/') // (상태, 제목, 주소)
	}

	await startWebSocketConnection()

	// // 해시를 확인했는데 로그인 되었는데 login 페이지로 가려고 하면 main 로 이동
	if (getSocketStatus() && location.hash === '#/login') {
		location.href = '/#/'
	}

	// 세션 스토리지에 로그인 정보가 없는데 /#/ 또는 /#/login이 아닌 경우 /#/ 페이지로 이동
	if (!getSocketStatus() && location.hash !== '#/' && location.hash !== '#/login' && location.hash !== '#/login/2fa') {
		location.href = '/#/'
	}

	const routerView = document.querySelector('router-view')
	const [hash, queryString = ''] = location.hash.split('?') // 물음표를 기준으로 해시 정보와 쿼리스트링을 구분
	// 2) 현재 라우트 정보를 찾아서 렌더링!
	const currentRoute = routes.find(route => new RegExp(`${route.path}/?$`).test(hash))
	routerView.innerHTML = ''
	routerView.append(new currentRoute.component().el)
}

export function createRouter(routes) {
	// 원하는(필요한) 곳에서 호출할 수 있도록 함수 데이터를 반환!
	return function () {
		window.addEventListener('popstate', () => {
			routeRender(routes)
		})
		routeRender(routes)
	}
}

export class Store {
	constructor(state) {
		this.state = {}
		this.observers = {}
		for (const key in state) {
			// 새로운 값이 할당될 때마다 함수를 호출하기 위해서
			Object.defineProperty(this.state, key, { // 객체 데이터의 속성을 정의
				get: () => state[key], // getter 함수
				set: val => { // setter 함수
					state[key] = val
					if (Array.isArray(this.observers[key])) { // 호출할 콜백이 있는 경우!
						this.observers[key].forEach(observer => observer(val))
					}
				}
			})
		}
	}
	subscribe(key, cb) { // 상태가 변경되는지 구독을 통해 감시하겠다. key, 함수 데이터 인자로 받음
		// 배열 데이터인지 확인
		Array.isArray(this.observers[key]) ? this.observers[key].push(cb) : this.observers[key] = [cb]
		// 배열 데이터에 함수를 여러개 넣어서 관리할 수 있도록
	}
}

export function selectProfileImg(profileImgIndex) {
	const profileImg = [
		'../public/images/charactors/pikachu.png',
		'../public/images/charactors/charmander.png',
		'../public/images/charactors/bulbasaur.png',
		'../public/images/charactors/squirtle.png',
		'../public/images/charactors/eevee.png',
		'../public/images/charactors/snorlax.png',
		'../public/images/charactors/mew.png',
		'../public/images/charactors/ditto.png',
	]
	return profileImg[profileImgIndex]
}

export function idValidationCheck(id) {
	const idPattern = /^[a-z0-9]{3,12}$/
	if (!idPattern.test(id)) {
		throw new Error('아이디는 3~12자의 영문 소문자와 숫자로만 입력해주세요.')
	}
}

export function passwordValidationCheck(password) {
	const passwordPattern = /^[a-zA-Z0-9]{4,8}$/
	if (!passwordPattern.test(password)) {
		throw new Error('비밀번호는 4~8자의 영문 대소문자와 숫자로만 입력해주세요.')
	}
}

function checkLength(state, key) {
	if (state.length > 10) {
	  throw new Error(`${key}는(은) 10자 이내로 입력해주세요.`);
	}
}
  
  function checkSpecialCharacters(state, key) {
	const allowedPattern = /^[a-zA-Z0-9ㄱ-ㅎ|ㅏ-ㅣ|가-힣\s-_.,?!]*$/;
	if (!allowedPattern.test(state)) {
	  throw new Error(`${key}에 허용되지 않은 특수문자가 포함되어 있습니다.`);
	}
}

export function stateValidationCheck(state, key) {
	const keyMapping = {
		'status_msg': '기분',
		'macrotext1': 'F1',
		'macrotext2': 'F2',
		'macrotext3': 'F3',
		'macrotext4': 'F4',
		'macrotext5': 'F5'
	};

	const displayKey = keyMapping[key] || key;
	checkLength(state, displayKey);
	checkSpecialCharacters(state, displayKey);
}