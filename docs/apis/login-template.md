# Login example

Used to collect a Token for a registered User.

**URL** : `/auth/`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "username": "[valid email address]",
    "password": "[password in plain text]"
}
```

**Data example**

```json
{
    "username": "sangnd",
    "password": "123456a@"
}
```

## Success Response

**Http Code** : `200 OK`

**Content example**

```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU0NDg1ODAxMywianRpIjoiZDlmZmU0M2NkNzQxNGNkMWIxMGRjOTZmMWFiNGQ4MTIiLCJ1c2VyX2lkIjoxfQ.Lds_MYLku7t7ojNwwL33st2TiTthsF-OWCRb8paV3Tk",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTQ0NzcxOTEzLCJqdGkiOiIxNjhkM2M1MWJiZDU0Nzg0OTk0MTU3M2IwNmFmNjc1ZSIsInVzZXJfaWQiOjF9.JOS8o3I9rwmFBk0GiQvXYzIoi3AGF8veKzugPR0Y5pU"
}
```

## Error Response
### Case 1
**Condition** : If 'username' and 'password' combination is wrong.

**Http Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "non_field_errors": [
        "No active account found with the given credentials"
    ]
}
```

### Case 2
**Condition** : No username and password in request.

**Http Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "username": [
        "This field is required."
    ],
    "password": [
        "This field is required."
    ]
}
```
### Case 3
**Condition** : Miss username in request.

**Http Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "username": [
        "This field is required."
    ]
}
```
### Case 4
**Condition** : Miss password in request.

**Http Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "password": [
        "This field is required."
    ]
}
```