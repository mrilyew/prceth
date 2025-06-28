import app from "../main.js"
import BaseController from "./BaseController.js"

export class AboutController extends BaseController {
    async main() {
        app.setContent(`
            <b>v0.0</b>
        `)
    }
}

export default AboutController
