import { createRouter } from "../core/core.js"
import Login from "./Login.js" // 로그인
import TwoFactorAuth from "./TwoFactorAuth.js";
import Home from "./Gate.js" // 게이트
import Main from "./Main.js" // 로비
import MyProfile from "./MyProfile.js" // 내 프로필
import { PingPongGame } from "../game/game.js" // 게임

export default createRouter([
	{ path: '#/', component: Home },
	{ path: '#/login', component: Login },
	{ path: '#/login/2fa', component: TwoFactorAuth },
	{ path: '#/main', component: Main },
	{ path: '#/myprofile', component: MyProfile },
	{ path: '#/game/onetoone/', component: PingPongGame },
	{ path: '#/game/tournament/', component: PingPongGame },
])