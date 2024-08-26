import { createRouter } from "../core/core.js"
import Login from "./Login.js" // 로그인
import Home from "./Gate.js" // 게이트
import Main from "./Main.js" // 로비

export default createRouter([
	{ path: '#/', component: Home },
	{ path: '#/login', component: Login },
	{ path: '#/main', component: Main }
])
