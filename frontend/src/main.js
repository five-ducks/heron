import App from "./App.js"
import router from "./routes/index.js"

const root = document.querySelector('#root')
root.append(new App().el)

router()
