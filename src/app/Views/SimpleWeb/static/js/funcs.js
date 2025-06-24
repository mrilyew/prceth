function escapeHtml(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;')
        .replace(/`/g, '&#x60;');
}

function collectParams(node) 
{
    pars = {}
    node.forEach(el => {
        let _name = el.querySelector("input[data-type='param_name']")
        let _val = el.querySelector("input[data-type='param_value']")

        pars[_name.value] = _val.value
    })

    return pars
}

function collectParamsByEach(node)
{
    pars = {}
    els = node.querySelectorAll("*[data-pname]")

    els.forEach(el => {
        pname = el.dataset.pname
        if (el.type == 'text' || el.type == 'number') {
            pars[pname] = el.value
        }

        if (el.type == 'checkbox') {
            pars[pname] = Number(el.checked)
        }
    })

    return pars
}
