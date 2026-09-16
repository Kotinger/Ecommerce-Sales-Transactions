# E-commerce Sales Transactions

Пет-проект: e-commerce аналитика от CSV до дашборда Power BI.  
Датасет: https://www.kaggle.com/datasets/miadul/e-commerce-sales-transactions-dataset  
Период: **сентябрь 2023 - сентябрь 2025** (хвост сентября 2025 неполный месяц).

Python -> MySQL -> Power BI. Метрики сверены между слоями.

---

## О чём проект

| Слой | Что делает |
|------|------------|
| **Python** | ETL, ключи, parquet, контрольные метрики |
| **SQL (MySQL)** | схема, load, sanity, KPI-запросы |
| **Power BI** | дашборд, 2 страницы |

**Маршрут: продажи (A)**
- **A - GMV, AOV, region, год x месяц** (+ срез category на дашборде)
- B - repeat, когорты, LTV (не делаем)
- C - маржа, топ SKU (не делаем)

**Метрики:** GMV = `SUM(total_amount)`, orders = `COUNT(DISTINCT order_key)`, AOV = GMV / orders.  
В этом датасете `order_key` = `order_id`.

**Зерно:** одна строка = один заказ (**order**). 34 500 строк = 34 500 `order_id`.

---

## Данные и ETL

Исходник в `data/`:

| Файл | Роль | строк |
|------|------|-------|
| `ecommerce_sales_34500.csv` | факт (заказ) | 34 500 |

17 колонок, пустых нет. Даты в ISO (`YYYY-MM-DD`).

**Чистка:** отмен и status нет; `total_amount > 0` (отвал 0); `order_date` -> datetime.  
`returned` в файле есть, в маршруте A не используем.

**Ключи:** `order_key` = `order_id` (один customer на order_id - 0 конфликтов).  
**people** не строим (`NEED_PEOPLE = False`).

---

## Ключевые находки

**Продажи**
- GMV **5 865 293.05**, заказов **34 500**, AOV **170.01**
- Регионы по GMV: South (1 298 096) / North (1 264 008) / West (1 186 350) / East (1 176 335) / Central (940 503)
- Пик месяца: **2024-12** (278 154). Хвост **2025-09** ниже полного месяца - не сравнивать с полными

**Категории**
- Лидер **Electronics** (3 319 207), дальше Home / Sports / Fashion / Beauty

Цифры совпадают в `scripts/report.py`, SQL (`04`-`06`) и карточках Power BI.

---

## Дашборд

Готовый отчёт: [`powerbi/Ecommerce_Dashboard.pbix`](powerbi/Ecommerce_Dashboard.pbix)

| Файл | Страница |
|------|----------|
| `powerbi/screenshots/01_overview.png` | Overview |
| `powerbi/screenshots/02_regions_products.png` | Regions & Products |

### Overview
![Overview](powerbi/screenshots/01_overview.png)

### Regions & Products
![Regions & Products](powerbi/screenshots/02_regions_products.png)

- **Overview** - карточки GMV / Orders / AOV; срезы region / Year; GMV по region; линия по месяцам
- **Regions & Products** - таблица region (GMV, Orders, AOV, %); доля GMV; GMV по category

---

## Pipeline


| Файл | Назначение |
|------|------------|
| `scripts/pipeline.py` | load, types, clean, `order_key`, parquet |
| `scripts/report.py` | GMV / AOV / region / year-month |
| `scripts/load_mysql.py` | parquet -> MySQL |
| `sql/01_schema.sql` | БД `ecommerce_sales` |
| `sql/02`-`03` | sanity, keys |
| `sql/04`-`06` | totals, region, year-month |

---

## Power BI - модель

Одна таблица `clean_orders` (Import). Связей нет.  
Ось месяцев: `YearMonth` как Date в Power Query для сортировки.

```dax
GMV = SUM ( 'clean_orders'[total_amount] )
Orders = DISTINCTCOUNT ( 'clean_orders'[order_key] )
AOV = DIVIDE ( [GMV], [Orders] )
GMV % of Total = DIVIDE ( [GMV], CALCULATE ( [GMV], ALLSELECTED ( 'clean_orders' ) ) )
```

---

## Стек

Python (pandas, pyarrow) -> MySQL 8 -> Power BI Desktop (DAX).

---

## Автор

@cat_main
