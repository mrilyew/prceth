import {proc_strtr, escapeHtml} from "../utils/utils.js"

class ContentUnitSmallViewModel {
    template(data) {
        return u(`
            <a href="#cu?uuids=${data.id}" class="scroll_element">
                <b>${proc_strtr(escapeHtml(data.display_name), 50)}</b>
            </a>
        `)
    }
}

export default ContentUnitSmallViewModel
