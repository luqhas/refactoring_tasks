# Задания

- Идентифицировать все случаи дублирования кода (code clone type I, II, III).
- Спроектировать абстрактный базовый класс AbstractReportGenerator с применением паттерна Template Method.
- Реализовать не менее 3 конкретных типов отчётов на основе базового класса.
- Добавить поддержку различных форматов вывода (text, CSV, HTML) через паттерн Strategy.
- Реализовать цепочку обработчиков (Chain of Responsibility) для постобработки отчётов: логирование, отправка email, архивирование.
- Провести измерение метрики WMC (Weighted Methods per Class) до и после рефакторинга.


## 1. Анализ дублирования

### 1-ый тип (Exact duplicates)
- StringBuilder sb = new StringBuilder();
- Period: from - to
- if (data.isEmpty()) { ... }
- logger.info(...)
- emailService.send(...)
- возврат sb.toString()

### 2-ой тип (Renamed variables/types)
- Sale vs Item
- getAmount() vs getStock()
- SQL-запросы отличаются только таблицей/полями
- email/subject разные

### 3-ий тип (Structural similarity)
- цикл обработки данных
- разная логика агрегации (total vs просто вывод)
- разный footer (Total vs Generated at)

---

## 2. WMC Метрики

### До
- Каждый класс в среднем: ~10–15
- Большая повторяемость

### После
- Абстрактный класс: ~6
- Остальные классы: ~3–4
- Обработчики/Стратегии: ~1