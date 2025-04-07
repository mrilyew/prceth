## Экстракторы

Экстракторы позволяют получить контент. Они возвращают словарь;
Словарь содержит ключи `entities` и, если подразумевается коллекция, `collection`.

`entities` является массивом из Entity. После выполнения execute() API меняет расположение файлов, добавляет Entity в Collection и т.д.
`collection`, если был возвращён, представляет из себя информацию в виде словаря коллекции, которая будет создана после завершения работы экстрактора.

### Класс

Экстрактор может находится в любой директории в `executables/extractors`, но лучше делить на поддиректорию, чтобы легче было ориентироваться. Например, если ваш экстрактор возвращает информацию о GitHub-репозитории, лучше создать директорию GitHub, в которой создать файл и класс Repo.

Экстрактор должен наследовать класс Base.

#### Параметры

Параметры экстрактора задаются с помощью статичной функции declare() в формате:
```
def declare():
    params = {}
    params[{name}] = {...}

    return params
```

По ключу задаётся словарь в формате:

`desc_key` — ключ локализации, отвечающий за описание параметра в интерфейсе

`type` — тип параметра. Возможные значения:

`int`, `float` — принимается число

`array` — Значение может быть только из перечисленных в массиве.

`string` — принимается строка

`object` — python объект; может быть задан только изнутри кода.

`bool` — false/true

---

`default` — какое значение будет задано при None

`hidden` — True/False; параметр скрыт из интерфейса

`assertion` — словарь, отвечающий за функцию assert:

`assert_not_null` со значением True — будет проверка значение на не равность None.

`assert_link` — значение будет привязано к указанному параметру, назовём X.

Если текущий параметр равен None, будет проверятся параметр X, если он тоже равен None, будет возвращено AssertionError.

---

`maxlength` — максимальная длина значения, только при `type` = `string`. 

Если в классе задан `manual_params`=True, будут переданы все переданные параметры, в том числе и недекларированные.

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
