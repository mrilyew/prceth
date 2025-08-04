### Overview

Модуль для сравнения настроек по умолчанию и приведённых. Из `app/App.py` доступно две переменные, `config` и `env`.

Основные настройки хранятся в `%storage%/settings/config.json`, информация для скриптов в `%storage%/settings/env.json`

#### Класс

##### get(option=,default=)

Получение настройки по имени.

##### set(option=,value=)

Изменение настройки.
