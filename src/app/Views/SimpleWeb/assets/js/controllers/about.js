import {_app, BaseController} from "../main.js"

export class AboutController extends BaseController {
    async main() {
        _app.setContent(`
            <b>v0.0</b>    
        `)
    }
}

export default AboutController
