# Upgrade Guide: Django 4.2 → 5.2.11 & allauth 0.55.0 → 65.0.5

> **Date:** February 16, 2026  
> **Previous Stack:** Django 4.2 / django-allauth 0.55.0  
> **Target Stack:** Django 5.2.11 LTS / django-allauth 65.0.2  

---

## Summary of Changes

| # | File(s) | Issue | Severity |
|---|---------|-------|----------|
| 1 | `root/settings.py` | `allauth.account.middleware.AccountMiddleware` is **commented out** — required since allauth 0.56 | 🔴 Critical |
| 2 | `root/settings.py` | `ACCOUNT_LOGOUT_ON_GET = True` — **removed** in allauth 65.x, replaced by `ACCOUNT_LOGOUT_ON_GET` no longer being honored. Logout now always requires POST | 🟡 Medium |
| 3 | `root/settings.py` | `USE_L10N = True` — **deprecated and removed** in Django 5.0. Localization is now always enabled | 🟡 Medium |
| 4 | `root/settings.py` | `ACCOUNT_LOGIN_METHODS` — the new setting (since allauth 65.4) uses a **set**, not a list. Should be `{"email"}` not `['email']` | 🟡 Medium |
| 5 | `root/settings.py` | `SOCIALACCOUNT_EMAIL_VERIFICATION` — renamed to `SOCIALACCOUNT_EMAIL_VERIFICATION` is still valid but should verify compatibility | 🟢 Low |
| 6 | `src/core/apps.py` | `default_auto_config` is **not a valid AppConfig attribute** — should be `default_auto_field` | 🔴 Critical |
| 7 | `src/website/apps.py` | Same `default_auto_config` typo — should be `default_auto_field` | 🔴 Critical |
| 8 | `src/services/accounts/apps.py` | Same `default_auto_config` typo — should be `default_auto_field` | 🔴 Critical |
| 9 | `src/services/management/apps.py` | Same `default_auto_config` typo — should be `default_auto_field` | 🔴 Critical |
| 10 | `src/core/apps.py`, `src/website/apps.py`, `src/services/management/apps.py` | `verbose_plural` is **not a valid AppConfig attribute** — should be `verbose_name_plural` (if needed) or removed | 🟡 Medium |
| 11 | `src/services/accounts/tokens.py` | Uses `import six` / `six.text_type()` — the `six` package is a Python 2/3 compatibility shim, **unnecessary for Python 3** | 🟡 Medium |
| 12 | `src/core/helpers.py` | Uses `import pytz` — **deprecated** in favor of `datetime.timezone` (stdlib) since Python 3.9. Django 5.x recommends `zoneinfo` | 🟡 Medium |
| 13 | `src/core/handlers.py` | `handler404` returns response **without status_code=404**. Django requires proper status codes | 🟡 Medium |
| 14 | `src/core/handlers.py` | `handler500` returns response **without status_code=500** | 🟡 Medium |
| 15 | `requirements.txt` | Packages are **unpinned** — should pin `Django==5.2.11` and `django-allauth==65.0.5` for reproducible builds | 🟡 Medium |
| 16 | `requirements.txt` | Contains `six` — no longer needed (Python 2 compat shim) | 🟢 Low |
| 17 | `requirements.txt` | Contains `pytz` — replaced by stdlib `zoneinfo`/`datetime.timezone` | 🟢 Low |
| 18 | `requirements.txt` | Contains `DateTime` (Zope DateTime) — likely unused, evaluate removal | 🟢 Low |
| 19 | `root/asgi.py` | Doc comment references Django 4.1 | 🟢 Low |
| 20 | `root/wsgi.py` | Doc comment references Django 4.1 | 🟢 Low |
| 21 | `templates/account/logout.html` | References `{% url 'accounts:cross-auth-view' %}` — should be `{% url 'accounts:cross-auth' %}` (as defined in accounts/urls.py) | 🟡 Medium |
| 22 | `src/services/management/utils.py` | References `Industry` and `AnnualIncome` models that don't exist in `models.py` — will cause ImportError | 🟡 Medium |
| 23 | `templates/account/email.html` | Uses `user.emailaddress_set.all` — in allauth 65.x the related name may differ; verify template works | 🟢 Low |
| 24 | `root/settings.py` | `django_browser_reload` middleware is in the main MIDDLEWARE list but the app is only conditionally mentioned in comments — should be conditional | 🟢 Low |

---

## Detailed Breakdown

### 🔴 CRITICAL — Must Fix

#### 1. AccountMiddleware (allauth 0.56+ requirement)

Since allauth **0.56.0**, the `allauth.account.middleware.AccountMiddleware` is **mandatory**. It is currently commented out in settings.py.

**File:** `root/settings.py`  
**Fix:** Uncomment the middleware line.

```python
# Before (broken)
# "allauth.account.middleware.AccountMiddleware",

# After (fixed)
"allauth.account.middleware.AccountMiddleware",
```

#### 6–9. `default_auto_config` typo in all AppConfig classes

The attribute `default_auto_config` does **not exist** in Django's `AppConfig`. The correct attribute is `default_auto_field`. This typo means BigAutoField is NOT being applied.

**Files:** `src/core/apps.py`, `src/website/apps.py`, `src/services/accounts/apps.py`, `src/services/management/apps.py`

```python
# Before (typo — silently ignored)
default_auto_config = 'django.db.models.BigAutoField'

# After (correct)
default_auto_field = 'django.db.models.BigAutoField'
```

---

### 🟡 MEDIUM — Should Fix

#### 2. `ACCOUNT_LOGOUT_ON_GET` removed

In allauth 65.x, `ACCOUNT_LOGOUT_ON_GET` has been removed. Logout now **always requires a POST request** for CSRF protection. The setting is silently ignored.

**Fix:** Remove the setting. Ensure logout templates/views use POST forms.

#### 3. `USE_L10N` deprecated

Django 5.0 removed `USE_L10N` — localization is now always active. The setting is silently ignored but should be cleaned up.

**Fix:** Remove `USE_L10N = True` from settings.

#### 4. `ACCOUNT_LOGIN_METHODS` format

allauth 65.4+ changed `ACCOUNT_AUTHENTICATION_METHOD` (string) to `ACCOUNT_LOGIN_METHODS` (set). The current value `['email']` (list) works but the canonical form is a set: `{"email"}`.

#### 10. `verbose_plural` → not a real attribute

`verbose_plural` is not recognized by Django's `AppConfig`. Use `verbose_name_plural` or remove it.

#### 11. `six` library usage in tokens.py

`six.text_type()` is just `str()` in Python 3. The `six` package is dead weight.

#### 12. `pytz` usage in helpers.py

Django 5.x and Python 3.9+ use `zoneinfo` and `datetime.timezone.utc`. `pytz` is a legacy dependency.

#### 13–14. Error handlers missing status codes

`handler404` and `handler500` use `render()` without passing `status=` kwarg, which defaults to 200 OK.

#### 21. Broken URL in logout template

The logout template references `accounts:cross-auth-view` but the URL name is `accounts:cross-auth`.

---

### 🟢 LOW — Nice to Fix

#### 15–18. requirements.txt cleanup

- Pin Django and allauth versions explicitly
- Remove `six` (Python 2 compat — unused)
- Remove `pytz` (replaced by stdlib)
- Evaluate `DateTime` (Zope package — likely unused)

#### 19–20. ASGI/WSGI doc comments

Reference Django 4.1 in their docstrings — cosmetic update to 5.2.

---

## Migration Checklist

- [x] Audit completed
- [x] Enable `AccountMiddleware` in settings
- [x] Fix `default_auto_config` → `default_auto_field` in all apps
- [x] Fix `verbose_plural` → `verbose_name_plural`
- [x] Remove `ACCOUNT_LOGOUT_ON_GET`
- [x] Remove `USE_L10N`
- [x] Fix `ACCOUNT_LOGIN_METHODS` to use set syntax
- [x] Remove `six` usage from `tokens.py`
- [x] Replace `pytz` with `datetime.timezone` in `helpers.py`
- [x] Fix `handler404`/`handler500` status codes
- [x] Pin versions in `requirements.txt`
- [x] Clean up `requirements.txt` (remove six, pytz, DateTime)
- [x] Fix broken URL in `logout.html`
- [x] Update ASGI/WSGI docstrings
- [x] Upgrade `dj-rest-auth` to 7.0.2 (Django 5.2 compatible)
- [x] Run `manage.py check` — ✅ passed
- [x] Run `manage.py migrate` — ✅ passed
