import { createRouter } from "../core/core.js"
import Login from "./Login.js" // 로그인
// import Lobby from "./Lobby.js" // 로비
import Gate from "./Gate.js" // 게이트

export default createRouter([
	{ path: '#/gate', component: Gate },
	{ path: '#/login', component: Login },
	// { path: '#/', component: Lobby }
])
