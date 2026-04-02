## Data Clumps

1. Банковские данные:

   * bankName
   * bankAccount
   * bankRoutingNumber

2. Адрес:

   * address
   * city
   * zipCode
   * country

3. Данные расчёта зарплаты:

   * baseSalary
   * overtimeHours
   * taxRate
   * pensionRate
   * healthInsuranceRate

---

## Рефакторинг

Применены следующие техники:

* Extract Class
* Move Method
* Value Object
* Принципы Law of Demeter

Выделены классы:

* SalaryCalculation
* BankDetails
* Address

## Применение Value Object

Классы Address и BankDetails:

* являются неизменяемыми
* используют `@dataclass(frozen=True)`
* имеют семантический equals и hash

---

## Закон Деметры

Соблюдён:

* Employee не обращается к внутренним полям зависимых объектов
* взаимодействие происходит через методы объектов

---

## Метрика LCOM

### До рефакторинга

* Методы используют разные наборы полей
* Минимальное пересечение
* LCOM высокий (низкая связность)

### После рефакторинга

* Логика разделена между классами
* Employee стал координирующим классом
* Связность внутри классов увеличилась
* LCOM уменьшился

---

## Вывод

Рефакторинг позволил:

* устранить Data Clumps
* снизить Feature Envy
* повысить когезию классов
* улучшить архитектуру системы
* привести код к принципам SOLID и Clean Code
