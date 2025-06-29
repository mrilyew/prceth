import {proc_strtr, escapeHtml} from "../utils/utils.js"

class ExecutableArgumentViewModel {
    template(data, argument_class) {
        const _f = u(`
            <div class="argument_listitem" data-name="${escapeHtml(data.name)}">
                <div class="argument_about">
                    <b>${proc_strtr(escapeHtml(data.name), 500)}</b>
                </div>
                <div class="argument_value"></div>
            </div>
        `)

        if (data.docs != null) {
            _f.find('.argument_about').append(`
                <p>${data.docs.definition ?? ''}</p>
            `)
        }

        if (argument_class != null) {
            _f.find(".argument_value").append(argument_class.renderValue(data)).attr("data-type", data.type)
        }

        return _f
    }
}

export default ExecutableArgumentViewModel
