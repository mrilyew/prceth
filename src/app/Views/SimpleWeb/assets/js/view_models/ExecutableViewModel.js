import {proc_strtr, escapeHtml} from "../utils/utils.js"

class ExecutableViewModel {
    template(data) {
        return u(`
            <a class="scroll_element no_overflow">
                <b>${data.class_name}</b>
            </a>
        `)
    }
}

export default ExecutableViewModel
