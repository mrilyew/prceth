Pretty ridiculous content extraction tool :h

Todo:

#### Экзекьютеблы

- [ ] Pre-execute если ничего не передано (?)
- [ ] Хуки выполнения
- [ ] Cli only use акты
- [ ] Кэширование списка
- [x] Разделить Executable на Runnable, Documentable, Saveable, RecursiveDeclarable
- [x] Игнорируемые параметры

#### Логирование

- [x] Логгирование запусков
- [ ] Максимальный размер лога?

#### Экспорт

- [ ] Acts.Export.Export (to .th zip)
- [ ] Acts.Export.Import
- [x] Acts.Export.CopyToDirectory
- [ ] Подмена даты создания файла при экспорте (если возможно?)

#### Contentunit

- [ ] Генерируемая колонка indexation_content_string (колонка `content` без ключей и пробелов)
- [x] Переписать превью
- [x] UUIDField вместо AutoField
- [ ] Подключение альтернативной базы данных по аргументу
- [x] Рефактор моделей
- [ ] Теги (?)
- [x] Основная ссылка

#### StorageUnit

- [x] Автоматическое определение размера файла
- [ ] Поиск дубликатов по хешу (?)
- [ ] Не переименовывать файл в хеш (?)

#### Declarable arguments

- [ ] Вынести проверку и assertions в отдельный метод?
- [ ] CsvArgument: не должен подразумевать строку но возможность задать тип

#### Репрезентации

- [x] Разделить репрезентацию и стратегию экспорта
- [x] Гидрация репрезентации
- [ ] Каждый метод репрезентации должен быть как то задокументирован и вынесен (?)
- [ ] Дополнительные методы репрезентации помимо экстракта
- [ ] "Универсальная" функция
- [ ] file_containment (?)

- [ ] Data.Hyperlink

#### Инциализация

- [ ] Адаптация под bash

#### Web crawler

- [ ] Переписать
- [ ] Режим archive.is без сохранения скриптов
- [ ] Определённые декларируемые функции для определённого сайта

#### Acts.ContentUnits.

- [x] Search
- [ ] Remove
- [x] GetById
- [ ] Edit

#### Acts.Links

- [ ] Link
- [ ] Unlink
- [ ] GetList
- [ ] GetListByItem
- [ ] ReoderLink

#### Acts.Executables.

- [x] List
- [ ] List занимает слишком много времени
- [x] Describe

#### Acts.Storage.

- [ ] ClearTemp

#### Acts.Metadata.

- [ ] для каждого mime-типа (?)

#### ContentUnitRelation

- [x] .is_revision
