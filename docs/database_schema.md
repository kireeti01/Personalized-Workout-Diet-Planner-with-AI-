# Database Design & ER Diagram

## ER Diagram (Mermaid)
```mermaid
erDiagram
    USERS ||--o{ PROFILES : has
    USERS ||--o{ RECOMMENDATIONS : generates
    
    USERS {
        int id PK
        string email UK
        string name
        string password_hash
        string created_at
    }
    
    PROFILES {
        int id PK
        int user_id FK
        int age
        string gender
        float height
        float weight
        float bmi
        string fitness_goal
        string activity_level
        string budget
        string dietary_preference
        string available_equipment
        string health_conditions
        string created_at
    }
    
    RECOMMENDATIONS {
        int id PK
        int user_id FK
        string workout_plan
        string meal_plan
        string recommended_at
    }
```

## SQL Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### Profiles Table
```sql
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    age INTEGER,
    gender TEXT,
    height REAL,
    weight REAL,
    bmi REAL,
    fitness_goal TEXT,
    activity_level TEXT,
    budget TEXT,
    dietary_preference TEXT,
    available_equipment TEXT,
    health_conditions TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
```

### Recommendations Table
```sql
CREATE TABLE recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    workout_plan TEXT,
    meal_plan TEXT,
    recommended_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
```

## Relationships
- A user can have one fitness profile at a time (1:1 relationship, but implemented as optional 1:0..1).
- A user can have multiple recommendations over time (1:M relationship).
- Profiles and recommendations are always tied to a user via foreign key constraints.
