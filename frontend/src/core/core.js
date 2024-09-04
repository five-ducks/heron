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

function routeRender(routes) {
	if (!location.hash) {
		history.replaceState(null, '', '/#/') // (상태, 제목, 주소)
	}
	// 쿠키를 통해 로그인 여부를 확인하고, 로그인이 되어 있지 않다면 gate 페이지로 이동
	if (getCookie('ppstate') != 200 && (location.hash !== '#/' && location.hash !== '#/login')) {
		location.href = '/#/login';
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