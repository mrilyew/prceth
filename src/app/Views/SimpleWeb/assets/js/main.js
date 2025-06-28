export const _app = new class {
    navigation = new class {
        setTab(tab) {
            u('#status-bar a').removeClass('selected')
            u(`#status-bar a[data-tab="${tab}"]`).addClass('selected')
        }
    }

    renderPage() {
        u('#app').html(`
            <nav id="status-bar">
                <a href="#about"><div id="home"></div></a>
                <a data-tab="content" class="tab" href="#content">Content</a>
                <a data-tab="exec" class="tab" href="#exec">Executables</a>
            </nav>
            <div id="container">
                <div id="page"></div>
            </div>
        `)
    }

    setContent(content = '') {
        u('#app #page').html(content)
    }
}

_app.renderPage()

export class BaseController {
    loader() {
        _app.setContent('...')
    }
}

export default _app
