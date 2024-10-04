from resources.consts import consts
from core.settings import settings
import i18n

localedir = consts['cwd'] + '\\localization\\langs'

i18n.load_path.append(localedir)
i18n.set('locale', settings.get('ui.lang'))

_ = i18n.t
