import { createRouter } from "../core/core"
import Login from "./Login" // 로그인
import Lobby from "./Lobby" // 로비
import Gate from "./gate" // 게이트

export default createRouter([
	{ path: '#/gate', component: Gate },
	{ path: '#/login', component: Login },
	{ path: '#/', component: Lobby }
])