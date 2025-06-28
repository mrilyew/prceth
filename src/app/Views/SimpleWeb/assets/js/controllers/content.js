import {_app, BaseController} from "../main.js"
import router from "../router.js"
import api from "../api.js"
import ContentUnitModel from "../models/ContentUnit.js"
import { escapeHtml } from "../utils.js"

const DEFAULT_COUNT = 100

export class ContentController extends BaseController {
    async main() {
        const items = await this.__items()
        const _u = u(`
            <div>
                <div id="container_body">
                    <!--<div id="container_head">
                        <b>${this.total_count} items</b>
                    </div>-->
                    <div id="container_items"></div>
                </div>
            </div>
        `)

        this.__push(items, _u)

        _app.setContent(_u.html())

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
            container.find("#container_items").append(itm.template())
        })

        if (this.scrolled_count < this.total_count) {
            container.find("#container_items").append(`
                <div class="show_more">Show next</div>    
            `)
        }
    }

    async __items(offset = null) {
        const items_resp = await api.act({
            "i": "ContentUnits.Search",
            "count": DEFAULT_COUNT,
            "timestamp_after": offset,
        })
        const payload = items_resp.payload
        const items = payload.items
        const total_count = payload.total_count

        this.total_count = total_count
        this.scrolled_count = (this.scrolled_count ?? 0) + items.length

        if (items[items.length - 1] != null) {
            this.last_offset = items[items.length - 1].created
        }

        return ContentUnitModel.fromArray(items)
    }

    async page() {
        const ids = router.url.getParam('uuids')
        const id_list = ids.split(',')
        const units = await ContentUnitModel.fromIds(id_list)
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

        _app.setContent(_u.html())
    }
}

export default ContentController
