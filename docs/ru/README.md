### База данных

Для сохранения контента используются ActiveRecord сущности из [Peewee](https://docs.peewee-orm.com/en/latest/): 

- [**ContentUnit**](db/content_unit.md) — единица контента в формате json
- [**StorageUnit**](db/storage_unit.md) — директория в %storage%, содержащая основной и дополнительные файлы. Может быть прикреплена к ContentUnit.
- [**ServiceInstance**](executables/service.md) — данные о Service

### Директории

%cwd% — папка установки

%storage% — %cwd%/storage/files. Может быть изменена в конфиге

### API

#### Командная строка

Акт выполняется через act.py:
```
cd [папка установки]
start.cmd
python act.py --i [имя акта] ...
```
