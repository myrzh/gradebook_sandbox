# gradebook_sandbox
## GradebookSandbox – Электронный журнал-песочница
GradebookSandbox – простое приложение для прогнозирования оценок в школе.
### Особенности
- Возможность добавлять предметы из представленного списка
- Возможность удалять предметы
- Возможность добавлять и удалять дополнительные столбцы
- Удобный редактор оценок с возможностью назначить коэффициент каждой оценке

Приложение использует формат __.CSV__ для хранения данных.
_Не загружайте в приложение таблицы, созданные в других приложениях!_
При введении некорретктных данных в клетку итоговая оценка для данного предмета изменится на __X.XX__.

Приложение загружает интерфейс из файлов __default_table.csv__, __main_window.ui__, __edit_subjects.ui__ и __subjects.sqlite__.
Эти файлы не предназначены для редактирования и всегда должны лежать в папке assets, находящейся в одной директории с исполняемым файлом.
