import {proc_strtr, escapeHtml} from "../utils.js"
import api from "../api.js"

class ContentUnitBigListView {
    template(data) {
        return u(`
            <a href="#cu?uuids=${data.id}" class="content_unit_item">
                <div class="content_unit_thumb">
                    <div class="content_unit_image"></div>
                </div>
                <div class="content_unit_info">
                    <b>${proc_strtr(escapeHtml(data.display_name), 50)}</b>
                    <div>
                        <span>${proc_strtr(escapeHtml(data.description ?? 'no desc'), 50)}</span>
                        <span>${escapeHtml(data.representation ?? '')}</span>
                    </div>
                </div>
            </a>
        `)
    }
}

class ContentUnitMiniListView {
    template(data) {
        return u(`
            <a href="#cu?uuids=${data.id}" class="content_unit_item_mini">
                <b>${proc_strtr(escapeHtml(data.display_name), 50)}</b>
            </a>
        `)
    }
}

export class ContentUnitModel {
    constructor(data) {
        this.data = data
        this.render_class = ContentUnitMiniListView
    }

    static fromArray(arr) {
        const f = []
        arr.forEach(el => {
            f.push(new ContentUnitModel(el))
        })

        return f
    }

    static async fromIds(ids) {
        const dl = await api.act({
            "i": "ContentUnits.GetById",
            "ids": ids,
        })
        const py = dl.payload

        return ContentUnitModel.fromArray(py)
    }

    template() {
        const data = this.data
        const _cl = new this.render_class()

        return _cl.template(data)
    }

}

export default ContentUnitModel
