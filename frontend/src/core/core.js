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

function routeRender(routes) {
	if (!location.hash) {
		history.replaceState(null, '', '/#/gate') // (상태, 제목, 주소)
	}
	const routerView = document.querySelector('router-view')
	const [hash, queryString = ''] = location.hash.split('?') // 물음표를 기준으로 해시 정보와 쿼리스트링을 구분
	// 2) 현재 라우트 정보를 찾아서 렌더링!
	console.log(hash)
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