import BaseController from "./BaseController.js"
import router from "../router.js"
import app from "../main.js"
import Executable from "../models/Executable.js"

const upper_categories = ["act", "extractor", "representation"]

export class ExecutableController extends BaseController {
    async main() {
        const _ap = u(`
            <div>
                <div class="horizontal_mini_tabs"></div>
                <div id="container_search">
                    <input placeholder="Search..." id="search_bar" type="search">
                </div>
                <div id="container_items"></div>
            </div>
        `)

        let current_tab = router.url.getParam('tab') ?? "act"
        if (!upper_categories.includes(current_tab)) {
            current_tab = "act"
        }

        upper_categories.forEach(exec_type => {
            _ap.find(".horizontal_mini_tabs").append(`
                <a data-tab="${exec_type}" href="#exec?tab=${exec_type}">${exec_type}s</a>
            `)

            if (current_tab == exec_type) {
                _ap.find(`.horizontal_mini_tabs a[data-tab="${current_tab}"]`).addClass("selected")
            }
        })

        const executables = await Executable.getList(current_tab)
        executables.forEach(el => {
            _ap.find("#container_items").append(el.render())
        })

        app.setContent(_ap.html())
    }
}

export default ExecutableController
