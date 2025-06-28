import {proc_strtr, escapeHtml} from "../utils/utils.js"

class ContentUnitBigViewModel {
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

export default ContentUnitBigViewModel
