# Accounts Service

A service a felhasználók regisztrációjáért, autentikációjáért és profilkezeléséért felelős.

Az autentikáció JWT-alapú:
- Az **access token** Bearer tokenként, az `Authorization` headerben küldendő.
- A **refresh token** HttpOnly cookie-ban tárolódik, ezért JavaScriptből nem érhető el.
- A lokális futtatáshoz kell egy ./config/appsettings.dev.json fájl:
```json
{
    "database":{
        "name": "db_name",
        "host": "host",
        "port": "db_port",
        "username": "dbuser",
        "password": "dbpassword"
    }
}
```

## API Endpoints

### `POST /register/`

Új felhasználó regisztrációja.

**Request:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "department": "Computer Science"
}
```

**Response – 201 Created:**
```json
{
  "message": "User registered successfully.",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    "department": "Computer Science",
    "role": {
      "id": 1,
      "role_name": "STUDENT",
      "display_name": "Student"
    },
    "is_active": true,
    "date_joined": "2026-11-07T12:00:00Z"
  }
}
```

A regisztrált felhasználó automatikusan `STUDENT` szerepkört kap.

### `POST /login/`

Felhasználó bejelentkeztetése e-mail-cím és jelszó alapján.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response – 200 OK:**
```json
{
  "user": {
    "id": 1,
    "username": "username",
    "role": "Student"
  },
  "access": "<access_token>"
}
```

A refresh token automatikusan `refresh_token` nevű HttpOnly cookie-ba kerül.

### `POST /token/refresh/`

Új access token igénylése a refresh token alapján.

**Request:**

A refresh token cookie automatikusan elküldésre kerül.

**Response – 200 OK:**
```json
{
  "access": "<new_access_token>"
}
```

Hiányzó vagy érvénytelen refresh token esetén `401 Unauthorized` választ ad.

### `POST /logout/`

Felhasználó kijelentkeztetése.

**Request:**

A refresh token cookie automatikusan elküldésre kerül.

**Response – 200 OK:**
```json
{
  "detail": "Logged out"
}
```

A refresh token blacklistelésre kerül, majd a cookie törlődik. A frontendnek az access tokent is törölnie kell.

### `GET /me/`

A bejelentkezett felhasználó profiladatainak lekérdezése.

**Header:**
```http
Authorization: Bearer <access_token>
```

**Response – 200 OK:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe",
  "department": "Computer Science",
  "role": {
    "id": 1,
    "role_name": "STUDENT",
    "display_name": "Student"
  },
  "is_active": true,
  "date_joined": "2026-11-07T12:00:00Z"
}
```

### `PATCH /me/`

A bejelentkezett felhasználó profiladatainak módosítása.

**Header:**
```http
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "first_name": "Jane",
  "department": "Software Engineering"
}
```

**Response – 200 OK:**

A módosított felhasználói profil adatai.

A módosítás csak a bejelentkezett felhasználóra vonatkozik. Az `is_active` és `date_joined` mezők nem módosíthatók.

### `DELETE /me/`

A bejelentkezett felhasználói fiók törlése.

**Header:**
```http
Authorization: Bearer <access_token>
```

A művelet kizárólag a bejelentkezett felhasználó saját fiókját törli.

## Megjegyzések

- A `/register/`, `/login/`, `/token/refresh/` és `/logout/` végpontok publikusak.
- A `/me/` végpontok autentikációt igényelnek.
- A refresh cookie `HttpOnly`, `Secure`, `SameSite=None` beállításokkal rendelkezik.
- A refresh token cookie élettartama 24 óra.
- A refresh token cookie path értéke: `/api/accounts/`.
- A cookie használatához a frontendnek engedélyeznie kell a credentialök küldését (`credentials: "include"`).
- A védett végpontokhoz érvényes access token szükséges.