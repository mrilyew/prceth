from components.consts import consts
from components.settings import settings
import i18n

localedir = consts['cwd'] + '\\locales'

i18n.load_path.append(localedir)
i18n.set('locale', settings.get('ui.lang'))

_ = i18n.t
