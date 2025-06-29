import BaseController from "./BaseController.js"
import router from "../router.js"
import app from "../main.js"
import api from "../api.js"
import Executable from "../models/Executable.js"
import subparams from "../utils/subparams.js"
import escapeHtml from "../utils/utils.js"

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

        const executables_list = await Executable.getList(current_tab)

        function __drawList(container, list) {
            list.forEach(el => {
                container.append(el.render())
            })
        }

        __drawList(_ap.find("#container_items"), executables_list)

        app.setContent(_ap.html())
        u('#container_search #search_bar').nodes[0].focus()
        u('#container_search').on('input', '#search_bar', (e) => {
            const query = e.target.value
            const itms = executables_list.filter(el => el.data.class_name.toLowerCase().includes(query))

            u("#container_items").html('')
            __drawList(u("#container_items"), itms)
        })
    }

    async executePage() {
        const exec_name = router.url.getParam('name')
        const extr = await Executable.getFromName(exec_name)
        const type = extr.sub
        const category = extr.category
        const name = extr.name
        const full_name = `${type}.${category}.${name}`
        const _ap = u(`
            <div>
                <div class="page-head">
                    <b>${escapeHtml(full_name)}</b>
                </div>
                <div class="page-subhead">
                    <span>${escapeHtml(extr.docs.definition ?? "")}</span>
                </div>
                <div id="args"></div>
                <div class="page-bottom">
                    <input id="exec" type="button" value="Execute">
                </div>
            </div>
        `)

        extr.args.forEach(arg => {
            if (arg.is_hidden) {
                return
            }

            _ap.find("#args").append(arg.render())
        })

        app.setContent(_ap.html())

        function collectArguments(nodes) {
            const vals = {}
            nodes.forEach(nd => {
                const val_node = nd.querySelector('.argument_value')
                const __type = val_node.dataset.type
                vals[nd.dataset.name] = subparams[__type].recieveValue(nd)
            })

            return vals
        }

        u(".page-bottom").on('click', '#exec', async (e) => {
            scrollTo(0, 0)

            const itms = u('#args .argument_listitem')
            const args = collectArguments(itms.nodes)

            u("#side").html("")

            const res = await api.executable(type.slice(0, type.length - 1), `${category}.${name}`, args)
            const jsonViewer = document.createElement("andypf-json-viewer")
            jsonViewer.data = res
            jsonViewer.expanded = true
            jsonViewer.indent = 4
            jsonViewer.expanded = 4
            jsonViewer.showDataTypes = false
            jsonViewer.showSize = false

            u("#side").append(jsonViewer)
        })
    }
}

export default ExecutableController
