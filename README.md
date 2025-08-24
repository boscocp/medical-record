# 🩺 Medical Records API

A system for managing medical records, supporting operations for inserting, updating, and querying patients, appointments, and patient records.

---

## 📦 Requirements

- Python **3.13**
- GCC **11**
- MySQL
- `pkg-config` (for native library integration)

### macOS Setup

```bash
brew install gcc@11
brew install mysql pkg-config
```

---

## ⚙️ Project Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/medical-records.git
cd medical-records
```

2. Install dependencies and set up the environment:

```bash
make setup
```

---

## 🗄️ Database Migrations (Alembic)

1. Create a new migration for the `person` table:

```bash
alembic revision -m "create persons table"
```

2. Apply the migration:

```bash
alembic upgrade head
```

---

## 🛢️ Connect to the Database

Connect to your local MySQL instance:

```bash
mysql -u localadmin -p -h 127.0.0.1 -P 3306 medical_record
```

Example query:

```sql
SELECT * FROM person LIMIT 10;
```

---

## 📤 Example Payload (Person)

```json
{
  "name": "João da Silva",
  "cpf": "12345678901",
  "civil_state": "S",
  "birth_date": "1990-05-15"
}
```

---

## 🧠 Data Model Overview

- **Person** : Basic personal information and marital status
- **Appointment** : Medical appointments (1:N relationship with Person)
- **PatientRecord** : Medical history (1:1 relationship with Person)

---

## 🧪 Running Tests

To run unit tests:

```bash
pytest
```
