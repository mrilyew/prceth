## Export.EntityToFS

Экспортирует Entity на диск.

Параметры:

`export_type` — "simple_grouping" или "full_stop".

`dir` — папка экспорта

`export_json` — экспортировать ли информацию об Entity в json файл.

`export_type`:

`simple_grouping` — Папки entity будут переименованы в свой id и перемещены в `dir`

`full_stop` (по умолчанию) — В папке `dir` будут созданы подпапки для каждой Entity. В ней — json информация и директория для прилинкованных Entity.
