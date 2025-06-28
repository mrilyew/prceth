import app from "../main.js"
import BaseController from "./BaseController.js"
import router from "../router.js"
import api from "../api.js"
import ContentUnit from "../models/ContentUnit.js"
import escapeHtml from "../utils/utils.js"

export class ContentController extends BaseController {
    async main() {
        const items = await this.__items()
        const insert_node = u(`
            <div>
                <div id="container_body">
                    <div id="container_items"></div>
                </div>
            </div>
        `)

        this.__push(items, insert_node)

        app.setContent(insert_node.html())

        u("#container_body").on("click", ".show_more", async (e) => {
            u(e.target).addClass('unclickable')

            const new_items = await this.__items(this.last_offset)
            const container = u(e.target).closest("#container_body")

            u(e.target).remove()
            this.__push(new_items, container)
        })
    }

    __push(items, container) {
        items.forEach(itm => {
            container.find("#container_items").append(itm.render())
        })

        if (this.scrolled_count < this.total_count) {
            container.find("#container_items").append(`
                <div class="show_more">Show next</div>    
            `)
        }
    }

    async __items(offset = null) {
        const response = await ContentUnit.search(100, offset)

        this.total_count = response.total_count
        this.scrolled_count = (this.scrolled_count ?? 0) + response.items.length

        return response.items
    }

    async page() {
        const ids = router.url.getParam('uuids')
        const id_list = ids.split(',')
        const units = await ContentUnit.fromIds(id_list)
        const _u = u(`
            <div>
                <div id="container_body">
                    <div id="container_items"></div>
                </div>
            </div>
        `)

        units.forEach(unit => {
            _u.find("#container_items").append(`
                <b>${escapeHtml(unit.data.display_name)}</b>
            `)
        })

        app.setContent(_u.html())
    }
}

export default ContentController
