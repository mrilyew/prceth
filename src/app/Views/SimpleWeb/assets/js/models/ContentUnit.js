import api from "../api.js"
import ContentUnitBigViewModel from "../view_models/ContentUnitBigViewModel.js"
import ContentUnitSmallViewModel from "../view_models/ContentUnitSmallViewModel.js"
import Model from "../models/Model.js"

export class ContentUnit extends Model {
    render_class = ContentUnitSmallViewModel

    static async fromIds(ids) {
        const dl = await api.act({
            "i": "ContentUnits.GetById",
            "ids": ids,
        })
        const py = dl.payload

        return ContentUnit.fromArray(py)
    }

    static async search(count = 100, offset = null) {
        const resp = await api.act({
            "i": "ContentUnits.Search",
            "count": count,
            "timestamp_after": offset ?? "",
        })
        const payload = resp.payload
        const items = payload.items
        let last_offset = null

        if (items[items.length - 1] != null) {
            last_offset = items[items.length - 1].created
        }

        return {
            "total_count": payload.total_count,
            "last_offset": last_offset,
            "items": ContentUnit.fromArray(items)
        }
    }
}

export default ContentUnit
