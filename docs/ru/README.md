### Overview

Prceth — python-приложение для организации и копирования контента.

#### Модели

[ContentUnit](models/content_unit.md)

`StorageUnit` (db/Models/Content) — представление директории с файлами из `storage/files/{00}`. Может содержать какое угодно количество файлов, но среди них должен быть основной.

#### Скрипты

[Скрипты](executables/README.md)

#### Запуск

Зависимости находятся в `requirements.txt`

Для входа в venv:

```
cd [папка установки]
.\venv.ps1
```

Для запуска act:

```
python act.py --i [имя акта] ...
```
