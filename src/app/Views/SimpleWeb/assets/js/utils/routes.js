import AboutController from "../controllers/AboutController.js"
import ContentController from "../controllers/ContentController.js"
import ExecutableController from "../controllers/ExecutableController.js"

export const routes = [
    {
        'route': 'index',
        'class': (new AboutController),
        'method': 'main'
    },
    {
        'route': 'content',
        'class': (new ContentController),
        'method': 'main'
    },
    {
        'route': 'cu',
        'class': (new ContentController),
        'method': 'page'
    },
    {
        'route': 'exec',
        'class': (new ExecutableController),
        'method': 'main'
    },
    {
        'route': 'execute',
        'class': (new ExecutableController),
        'method': 'executePage'
    },
]

export default routes
