import app from "../main.js"

export class BaseController {
    loader() {
        app.setContent('...')
    }
}

export default BaseController
