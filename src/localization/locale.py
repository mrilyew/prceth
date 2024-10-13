from resources.globals import i18n, settings, consts

localedir = consts['cwd'] + '\\localization\\langs'

i18n.load_path.append(localedir)
i18n.set('locale', settings.get('ui.lang'))

_ = i18n.t
