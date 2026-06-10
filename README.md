# Fast Account 2 — فاست أكاونت 2

**Restaurant POS & Management System** | **نظام إدارة مطاعم ونقطة بيع**

A full-featured restaurant management desktop application built with Python and PyQt5, connected to a MySQL database. Handles cashier operations (ordering, billing, invoicing), employee management (attendance, payroll), expense/revenue tracking, delivery management, table management, and financial reporting.

---

## Features | المميزات

- **Cashier / POS** — Departments & products management, order placement, table/delivery/takeaway modes, tax & discount, cash/visa payment, PDF invoice printing
- **Employee Management** — Add/search/update employees, attendance tracking, monthly salary calculation with bonuses & deductions
- **Expenses & Revenues** — Daily recording of expenses and revenues, delivery location management
- **Sales Reports** — Daily/monthly/yearly unit sales, daily cash/visa revenue, cashier shift summary, income statements
- **Tables Management** — Visual table toggle (occupied/free) with state persistence
- **Access Control** — Admin and User roles with password protection

---

## Tech Stack | التقنيات المستخدمة

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12+ |
| GUI | PyQt5 5.15.11 |
| Database | MySQL (`mysql-connector-python`) |
| PDF | ReportLab (`reportlab`) |
| Arabic Text | `arabic_reshaper`, `python-bidi` |
| UI Design | Qt Designer (`.ui` / `pyuic5`) |

---

## Setup | الإعداد والتشغيل

### Prerequisites | المتطلبات

- Python 3.12+
- MySQL server running at `192.168.1.7:3306` with a database named `restaurant`
- *(Or update the connection parameters in `main.py:24-30`)*

### Installation

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already in venv)
pip install reportlab arabic-reshaper python-bidi
```

### Run

```bash
python main.py
```

### Login | تسجيل الدخول

| Role | Password |
|------|----------|
| Admin | `admin` |
| User | `user` |

### Build Executable

```bash
pyinstaller --onefile --noconsole main.py
```

---

## Database | قاعدة البيانات

The app auto-creates tables in the `restaurant` database on startup, including: `departments`, `products`, `employees`, `expenses`, `revenues`, `delivery`, `taxes`, `newShift`, `numberOFUnits`, `MnumberOFUnits`, `YnumberOFUnits`, `departmentsTables`, `productsTables`, `bonusOrDeduct`, `revenuesVisa`.

---

## Project Structure | هيكل المشروع

```
FastAccount_2/
├── main.py              # Application entry point
├── cashierpro_ui.py     # Compiled Qt Designer UI
├── cashierpro.ui        # Qt Designer source
├── icon_rc.py           # Compiled resource file
├── icon.qrc             # Qt resource collection
├── Amiri-Regular.ttf    # Arabic font for PDF invoices
├── table_states.json    # Persisted table occupancy
├── myInvoice.pdf        # Generated invoice output
├── .gitignore
└── venv/                # Python virtual environment
```

---

## Developer | المطور

**Marwan Ashraf**

---

## License | الترخيص

All rights reserved.
