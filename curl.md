# Expense Tracker API - cURL Commands

Base URL:

```
http://127.0.0.1:8000
```

---

# Expense Lifecycle

## 1. Create Expense

Creates a new expense.

```bash
curl -X POST http://127.0.0.1:8000/expenses \
-H "Content-Type: application/json" \
-d '{
    "amount":200,
    "description":"Coffee",
    "spent_on":"2026-03-10",
    "category_id":1
}'
```

Expected response:

```json
{
    "id": 1,
    "amount": 200,
    "description": "Coffee",
    "spent_on": "2026-03-10",
    "category": {
        "id": 1,
        "name": "Food"
    }
}
```

---

## 2. Fetch Expense

Fetch the created expense using its id.

```bash
curl http://127.0.0.1:8000/expenses/1
```

Expected response:

```json
{
    "id":1,
    "amount":200,
    "description":"Coffee",
    "spent_on":"2026-03-10",
    "category":{
        "id":1,
        "name":"Food"
    }
}
```

---

## 3. Update Expense

Updates the expense details.

```bash
curl -X PUT http://127.0.0.1:8000/expenses/1 \
-H "Content-Type: application/json" \
-d '{
    "amount":300,
    "description":"Updated Coffee",
    "spent_on":"2026-03-15",
    "category_id":1
}'
```

Expected response:

```json
{
    "id":1,
    "amount":300,
    "description":"Updated Coffee",
    "spent_on":"2026-03-15",
    "category":{
        "id":1,
        "name":"Food"
    }
}
```

---

## 4. Delete Expense

Deletes the expense.

```bash
curl -X DELETE http://127.0.0.1:8000/expenses/1
```

Expected response:

```
204 No Content
```

---

# Additional API Checks

## Get All Expenses

```bash
curl http://127.0.0.1:8000/expenses
```

---

## Filter Expenses

Example: Food expenses in March 2026.

```bash
curl "http://127.0.0.1:8000/expenses?category_id=1&from_date=2026-03-01&to_date=2026-03-31"
```

---

## Get All Categories

```bash
curl http://127.0.0.1:8000/categories
```

---

## Get Category By ID

```bash
curl http://127.0.0.1:8000/categories/1
```

---

## Create Category

```bash
curl -X POST http://127.0.0.1:8000/categories \
-H "Content-Type: application/json" \
-d '{
    "name":"Shopping"
}'
```

---

## Update Category

```bash
curl -X PUT http://127.0.0.1:8000/categories/1 \
-H "Content-Type: application/json" \
-d '{
    "name":"Food Updated"
}'
```

---

## Delete Category

```bash
curl -X DELETE http://127.0.0.1:8000/categories/5
```

---

## Monthly Summary

```bash
curl "http://127.0.0.1:8000/summary?month=2026-03"
```