## Экстракторы

Экстракторы позволяют получить контент. Они возвращают словарь;
Словарь содержит ключи `entities` и, если подразумевается коллекция, `collection`.

`entities` является массивом из Entity. После выполнения execute() API меняет расположение файлов, добавляет Entity в Collection и т.д.
`collection`, если был возвращён, представляет из себя информацию в виде словаря коллекции, которая будет создана после завершения работы экстрактора.

### Класс

Экстрактор может находится в любой директории в `executables/extractors`, но лучше делить на поддиректорию, чтобы легче было ориентироваться. Например, если ваш экстрактор возвращает информацию о GitHub-репозитории, лучше создать директорию GitHub, в которой создать файл и класс Repo.

Экстрактор должен наследовать класс Base.

#### Методы

**__init__(temp_dir=,del_dir_on_fail=,need_preview=)**

`temp_dir` = временная папка во время выполнения Extractor'а
`del_dir_on_fail` = удалить ли папку при неудаче
`need_preview` = нужно ли превью

**setArgs()**

Задаёт параметры

**_fileFromJson({})**
**_entityFromJson({})**
**_collectionFromJson({})**

**run()** *async*

Выполняет действия экстрактора

**postRun()** *async*

Выполняет действия после основного

**thumbnail()**

Создаёт превью для полученных Entity

**execute()**

Более краткий run()

#### Шаблон

```
    from executables.extractors.Base import BaseExtractor

    class Template(BaseExtractor):
        name = 'template'
        category = 'template'
        params = {}

        def setArgs(self, args):
            self.passed_params = args

            super().setArgs(args)

        def onFail(self):
            pass

        async def run(self, args):
            pass

        async def postRun(self):
            pass
```
