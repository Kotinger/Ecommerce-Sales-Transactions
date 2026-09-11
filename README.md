# E-commerce Sales Transactions

Пет-проект: e-commerce аналитика от CSV до дашборда Power BI.  
Датасет: https://www.kaggle.com/datasets/miadul/e-commerce-sales-transactions-dataset  

Период: **2023–2025** (хвост сентября 2025 — неполный месяц).

Python → MySQL → Power BI. Метрики сверены между слоями.

---

## О чём проект

| Слой | Что делает |
|------|------------|
| **Python** | ETL, ключи, parquet, контрольные метрики |
| **SQL (MySQL)** | схема, sanity, KPI-запросы |
| **Power BI** | дашборд, 2 страницы |

**Маршрут ABC:-> A**
- **A — GMV, AOV, region, месяцы** 
- B — repeat, когорты, LTV 
- C — маржа, топ товары 

**Метрики:** GMV = `SUM(total_amount)`, AOV = GMV / orders.  
Заказы считаем по **`order_key`** (в SQL и Power BI); в этом датасете `order_key` = `order_id`.

---

## Данные и ETL

Исходник: **34 500 строк**, 17 колонок, пустых нет. Даты в ISO (`YYYY-MM-DD`).

**Зерно — order** (одна строка = один заказ): 34 500 строк = 34 500 `order_id`.

**Чистка:**
- отмен и status в данных нет
- `total_amount <= 0` — отфильтровано → **34 500** строк clean (все суммы > 0)
- `order_date` → `datetime`
- `returned` есть, в маршруте A не используем

**Ключи** (в `pipeline.py`):
- `order_key` = `order_id` (проверка: один customer на order_id — 0 конфликтов)
- `people` / `customer_key` не строим (`NEED_PEOPLE = False`)

---

## Главное 

- Оборот **~5.87M** на **34 500** заказах, средний чек **~170**.
- Регионы по GMV: **South → North → West → East → Central**.
- Пик месяца: **декабрь 2024** (~278K). Сентябрь 2025 обрезан — с полными месяцами не сравнивать.
- По категориям лидер — **Электроника** (~3.3M).

### Ключевые цифры

| Метрика | Значение |
|---------|----------|
| GMV | 5 865 293 |
| Orders | 34 500 |
| AOV | ~170 |
| Пик месяца | 2024-12 (~278K) |
| Топ region | South |

Цифры совпадают в `report.py`, SQL (`04_kpi_totals`) и карточках Power BI.

---

## Дашборд

| Файл | Страница |
|------|----------|
| `powerbi/screenshots/01_overview.png` | Overview |
| `powerbi/screenshots/02_regions_products.png` | Regions & Products |

### Overview
![Overview](powerbi/screenshots/01_overview.png)

### Regions & Products
![Regions & Products](powerbi/screenshots/02_regions_products.png)

Готовый отчёт: `powerbi/Ecommerce_Dashboard.pbix`

- **Overview** — GMV, Orders, AOV + срезы region / Year + GMV по region + динамика по месяцам
- **Regions & Products** — таблица region (GMV, Orders, AOV, %), доля GMV, GMV по category

---

## Pipeline

```text
data/ecommerce_sales_34500.csv
        │
        ├─► scripts/pipeline.py  -  clean + keys → data/processed/*.parquet
        ├─► scripts/report.py  -  метрики маршрута A, сверка
        ├─► scripts/load_mysql.py  -  parquet → MySQL (ecommerce_sales)
        ├─► sql/01_schema.sql … 06  -  sanity, keys, KPI
        └─► powerbi/  -  дашборд + скрины
```

| Файл | Назначение |
|------|------------|
| `scripts/pipeline.py` | загрузка, типы, чистка, `order_key`, parquet |
| `scripts/report.py` | GMV / AOV / region / year-month |
| `scripts/load_mysql.py` | parquet → MySQL |
| `sql/01_schema.sql` | база `ecommerce_sales`, `clean_orders` |
| `sql/02_sanity.sql` | проверки после загрузки |
| `sql/03_keys.sql` | проверка ключей |
| `sql/04`–`06_kpi_*.sql` | totals, region, year-month |

---

## Power BI — модель

Одна таблица `clean_orders` (Import). Связей нет — `YearMonth` как Date в Power Query для сортировки оси.

```dax
GMV = SUM('clean_orders'[total_amount])
Orders = DISTINCTCOUNT('clean_orders'[order_key])
AOV = DIVIDE([GMV], [Orders])
GMV % of Total = DIVIDE([GMV], CALCULATE([GMV], ALLSELECTED('clean_orders')))
```

---

## Стек

Python (pandas, pyarrow) → MySQL 8 → Power BI Desktop (DAX).


---

## Автор

@cat_main
