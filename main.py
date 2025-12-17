from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy import text

from database import SessionLocal  # твой файл с подключением к SQL Server

import random
import math
from datetime import date


# ================== КОНФИГ ГРУПП И ТАБЛИЦ ===================

GROUP_TABLES = {
    'AdminUsers': '[dbo].[AdminUsers]',
    'DT-311b': '[dbo].[DT-311b]',
    'DT-411b': '[dbo].[DT-411b]',
    'DT-42b': '[dbo].[DT-42b]',
    'DT-511b': '[dbo].[DT-511b]',
    'GD-314b': '[dbo].[GD-314b]',
    'GD-411b': '[dbo].[GD-411b]',
    'GD-412b': '[dbo].[GD-412b]',
    'GD-413b': '[dbo].[GD-413b]',
    'GD-511b': '[dbo].[GD-511b]',
    'GD-512b': '[dbo].[GD-512b]',
    'GD-513b ': '[dbo].[GD-513b ]',
    'IN-311b': '[dbo].[IN-311b]',
    'IN-312b': '[dbo].[IN-312b]',
    'IN-411b': '[dbo].[IN-411b]',
    'IN-412b': '[dbo].[IN-412b]',
    'IN-413b': '[dbo].[IN-413b]',
    'IN-41b': '[dbo].[IN-41b]',
    'IN-511b': '[dbo].[IN-511b]',
    'IN-512b': '[dbo].[IN-512b]',
    'IN-51b': '[dbo].[IN-51b]',
    'IS-311b': '[dbo].[IS-311b]',
    'IS-411b': '[dbo].[IS-411b]',
    'IS-412b': '[dbo].[IS-412b]',
    'IS-413b': '[dbo].[IS-413b]',
    'IS-511b': '[dbo].[IS-511b]',
    'IS-512b': '[dbo].[IS-512b]',
    'R-511b': '[dbo].[R-511b]',
    'RCAS-511b': '[dbo].[RCAS-511b]',
    'RCAS-513b': '[dbo].[RCAS-513b]',
    'RCAS-51b': '[dbo].[RCAS-51b]',
    'RET-311b': '[dbo].[RET-311b]',
    'RET-411b': '[dbo].[RET-411b]',
    'RET-412b': '[dbo].[RET-412b]',
    'RET-413b': '[dbo].[RET-413b]',
    'RET-41b': '[dbo].[RET-41b]',
    'RET-43b': '[dbo].[RET-43b]',
    'RET-511b': '[dbo].[RET-511b]',
    'RET-512b': '[dbo].[RET-512b]',
    'RET-51b': '[dbo].[RET-51b]',
    'S-411б': '[dbo].[S-411б]',
    'S-413б': '[dbo].[S-413б]',
    'S-511б': '[dbo].[S-511б]',
    'S-513б': '[dbo].[S-513б]',
    'S-51б': '[dbo].[S-51б]',
    'SW-311b': '[dbo].[SW-311b]',
    'SW-312b': '[dbo].[SW-312b]',
    'SW-313b': '[dbo].[SW-313b]',
    'SW-315b': '[dbo].[SW-315b]',
    'SW-319b': '[dbo].[SW-319b]',
    'SW-321b': '[dbo].[SW-321b]',
    'SW-411b': '[dbo].[SW-411b]',
    'SW-412b': '[dbo].[SW-412b]',
    'SW-413b': '[dbo].[SW-413b]',
    'SW-414b': '[dbo].[SW-414b]',
    'SW-415b': '[dbo].[SW-415b]',
    'SW-416b': '[dbo].[SW-416b]',
    'SW-417b': '[dbo].[SW-417b]',
    'SW-419b': '[dbo].[SW-419b]',
    'SW-421b': '[dbo].[SW-421b]',
    'SW-423b': '[dbo].[SW-423b]',
    'SW-425b': '[dbo].[SW-425b]',
    'SW-43b': '[dbo].[SW-43b]',
    'SW-45b': '[dbo].[SW-45b]',
    'SW-46b': '[dbo].[SW-46b]',
    'SW-511b': '[dbo].[SW-511b]',
    'SW-512b': '[dbo].[SW-512b]',
    'SW-513b': '[dbo].[SW-513b]',
    'SW-514b': '[dbo].[SW-514b]',
    'SW-515b': '[dbo].[SW-515b]',
    'SW-517b': '[dbo].[SW-517b]',
    'SW-51b': '[dbo].[SW-51b]',
    'SW-53b': '[dbo].[SW-53b]',
    'SW-55b': '[dbo].[SW-55b]',
    'SW-57b': '[dbo].[SW-57b]',
    'ПАТ-51б': '[dbo].[ПАТ-51б]',
    'ПВ-31б': '[dbo].[ПВ-31б]',
    'ПВ-41б': '[dbo].[ПВ-41б]',
    'ПЭ-52б': '[dbo].[ПЭ-52б]',
    'Р-511b': '[dbo].[Р-511b]',
    'С-311б': '[dbo].[С-311б]',
    'С-313б': '[dbo].[С-313б]',
    'С-41b': '[dbo].[С-41b]',
    'С-53б': '[dbo].[С-53б]',
}

ADMIN_TABLE = '[dbo].[AdminUsers]'
ATTENDANCE_TABLE = '[dbo].[AttendanceMarks]'   # таблица для записей посещаемости


# ================== МОТИВАЦИОННЫЕ ФРАЗЫ ===================

MOTIVATION_RU = [
    "Отличный выбор — прийти сегодня! Маленький шаг к большой цели.",
    "Каждая пара — это инвестиция в твое будущее.",
    "Ты сегодня уже на шаг впереди тех, кто не пришел.",
    "Знания — это сила. Ты только что усилил себя ещё на +1.",
    "Умные не те, кто всё знает, а те, кто приходит учиться.",
]

MOTIVATION_KZ = [
    "Бүгін келген әр күнің — болашағыңа салынған инвестиция.",
    "Білімге келген қадам — табысқа жақындаған қадам.",
    "Сабаққа келу — өзіңе жасаған ең жақсы сыйлық.",
    "Бүгінгі қатысу — ертеңгі мүмкіндігің.",
    "Оқыған адам – озған адам. Бүгін тағы бір қадам жасалды.",
]


# ================== ГЕОЛОКАЦИЯ КОЛЛЕДЖА ===================

COLLEGE_LAT = 45.011600680065506
COLLEGE_LON = 78.35112952775499
ALLOWED_RADIUS_METERS = 250  # радиус, в котором засчитываем посещение


def distance_meters(lat1, lon1, lat2, lon2) -> float:
    R = 6371000  # м
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# ================== БД ===================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================== ЯЗЫК / DEVICE ===================

def get_lang(request: Request) -> str:
    lang = request.cookies.get("lang", "ru")
    if lang not in ("ru", "kz"):
        lang = "ru"
    return lang


def is_desktop(request: Request) -> bool:
    ua = (request.headers.get("user-agent") or "").lower()
    return not any(x in ua for x in ["mobile", "android", "iphone"])


# ================== FASTAPI ===================

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ================== ЯЗЫК ===================

@app.get("/set-lang/{lang_code}")
async def set_lang(lang_code: str, request: Request):
    lang = "kz" if lang_code.lower() == "kz" else "ru"
    referer = request.headers.get("referer") or "/"
    response = RedirectResponse(url=referer, status_code=302)
    response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365)
    return response


# ================== ГЛАВНАЯ ===================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    lang = get_lang(request)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "lang": lang},
    )


# ================== ВХОД СТУДЕНТА ===================

@app.get("/login", response_class=HTMLResponse)
async def student_login_get(request: Request):
    lang = get_lang(request)
    desktop = is_desktop(request)
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "lang": lang,
            "is_desktop": desktop,
            "error": None,
            "success": None,
        },
    )


@app.post("/login", response_class=HTMLResponse)
async def student_login_post(
    request: Request,
    login: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    lang = get_lang(request)
    desktop = is_desktop(request)

    print(f"[DEBUG] STUDENT LOGIN TRY: {login!r}")

    found = None
    found_group = None

    for group_name, table in GROUP_TABLES.items():
        if group_name == "AdminUsers":
            continue

        sql = text(f"""
            SELECT TOP 1 *
            FROM {table}
            WHERE [LoginName] = :login
              AND [PasswordPlain] = :password
        """)
        try:
            row = db.execute(sql, {"login": login, "password": password}).fetchone()
            print(f"[DEBUG] Checked {table}, result={bool(row)}")
        except Exception as e:
            print(f"[DEBUG] SQL ERROR in {table}: {e}")
            continue

        if row:
            found = row
            found_group = group_name
            break

    if not found:
        error_msg = "Неверный логин или пароль." if lang == "ru" else "Логин немесе құпиясөз қате."
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "lang": lang,
                "is_desktop": desktop,
                "error": error_msg,
                "success": None,
            },
        )

    motivation = random.choice(MOTIVATION_RU if lang == "ru" else MOTIVATION_KZ)

    return templates.TemplateResponse(
        "mark.html",
        {
            "request": request,
            "lang": lang,
            "login": login,
            "group_name": found_group,
            "motivation_preview": motivation,
            "error_msg": None,
            "success_msg": None,
        },
    )


# ================== ОТМЕТКА С ГЕОЛОКАЦИЕЙ ===================

@app.post("/mark", response_class=HTMLResponse)
async def mark_attendance(
    request: Request,
    login: str = Form(...),
    group_name: str = Form(...),
    lat: str = Form(None),
    lon: str = Form(None),
    accuracy: str = Form(None),
    db: Session = Depends(get_db),
):
    lang = get_lang(request)

    print(f"[DEBUG] MARK TRY: login={login!r}, group={group_name!r}, lat={lat}, lon={lon}, acc={accuracy}")

    def msg(key: str) -> str:
        ru = {
            "geo_required": "Нужно включить геолокацию и разрешить доступ к местоположению.",
            "geo_outside": "Вы находитесь вне территории колледжа. Отметка не принята.",
            "geo_failed": "Не удалось определить местоположение. Попробуйте ещё раз.",
            "mark_error": "Не удалось сохранить отметку. Обратитесь к куратору.",
            "mark_already": "Вы уже отметились сегодня.",
            "mark_success": "Отметка сохранена! Хорошей пары!",
        }
        kz = {
            "geo_required": "Геолокацияны қосып, орналасуға рұқсат беру қажет.",
            "geo_outside": "Сіз колледж аумағынан тыс жердесіз. Белгі қабылданбады.",
            "geo_failed": "Орналасуды анықтау мүмкін болмады. Қайталап көріңіз.",
            "mark_error": "Қатысуды сақтау мүмкін болмады. Кураторға хабарласыңыз.",
            "mark_already": "Бүгін қатысуды бұрыннан белгілеп қойғансыз.",
            "mark_success": "Қатысу сәтті белгіленді! Сабақ сәтті өтсін!",
        }
        return (ru if lang == "ru" else kz)[key]

    def render(error=None, success=None, motivation=None):
        if motivation is None:
            motivation = random.choice(MOTIVATION_RU if lang == "ru" else MOTIVATION_KZ)
        return templates.TemplateResponse(
            "mark.html",
            {
                "request": request,
                "lang": lang,
                "login": login,
                "group_name": group_name,
                "motivation_preview": motivation,
                "error_msg": error,
                "success_msg": success,
            },
        )

    # Геолокация
    try:
        lat_val = float(lat) if lat is not None else None
        lon_val = float(lon) if lon is not None else None
    except Exception:
        lat_val = lon_val = None

    if lat_val is None or lon_val is None:
        return render(error=msg("geo_required"))

    dist = distance_meters(lat_val, lon_val, COLLEGE_LAT, COLLEGE_LON)
    print(f"[DEBUG] Distance to college: {dist:.2f} m")

    if dist > ALLOWED_RADIUS_METERS:
        return render(error=msg("geo_outside"))

    # Проверяем, что студент реально есть в своей группе
    table = GROUP_TABLES.get(group_name)
    if not table or group_name == "AdminUsers":
        return render(error=msg("mark_error"))

    check_sql = text(f"""
        SELECT TOP 1 *
        FROM {table}
        WHERE [LoginName] = :login
    """)
    try:
        student_row = db.execute(check_sql, {"login": login}).fetchone()
    except Exception as e:
        print(f"[DEBUG] SQL ERROR (check student) in {table}: {e}")
        return render(error=msg("mark_error"))

    if not student_row:
        return render(error=msg("mark_error"))

    # Уже отметился сегодня?
    today = date.today()

    already_sql = text(f"""
        SELECT TOP 1 *
        FROM {ATTENDANCE_TABLE}
        WHERE [LoginName] = :login
          AND [GroupName] = :group_name
          AND [MarkDate] = :mark_date
    """)

    already = db.execute(already_sql, {
        "login": login,
        "group_name": group_name,
        "mark_date": today,
    }).fetchone()

    if already:
        return render(error=msg("mark_already"))

    # Сохраняем отметку
    motivation = random.choice(MOTIVATION_RU if lang == "ru" else MOTIVATION_KZ)

    insert_sql = text(f"""
        INSERT INTO {ATTENDANCE_TABLE} (LoginName, GroupName, MarkDate, Status, MotivationText)
        VALUES (:login, :group_name, :mark_date, :status, :motivation)
    """)

    try:
        db.execute(insert_sql, {
            "login": login,
            "group_name": group_name,
            "mark_date": today,
            "status": "present",
            "motivation": motivation,
        })
        db.commit()
        print("[DEBUG] Mark inserted successfully")
    except Exception as e:
        db.rollback()
        print(f"[DEBUG] ERROR inserting mark: {e}")
        return render(error=msg("mark_error"), motivation=motivation)

    return render(success=msg("mark_success"), motivation=motivation)


# ================== ВХОД АДМИНА ===================

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_get(request: Request):
    lang = get_lang(request)
    return templates.TemplateResponse(
        "admin_login.html",
        {"request": request, "lang": lang, "error": None},
    )


@app.post("/admin/login", response_class=HTMLResponse)
async def admin_login_post(
    request: Request,
    login: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    lang = get_lang(request)
    print(f"[DEBUG] ADMIN LOGIN TRY: {login!r}")

    sql = text(f"""
        SELECT TOP 1 *
        FROM {ADMIN_TABLE}
        WHERE [LoginName] = :login
          AND [PasswordPlain] = :password
    """)

    try:
        row = db.execute(sql, {"login": login, "password": password}).fetchone()
        print(f"[DEBUG] Admin row found: {bool(row)}")
    except Exception as e:
        print(f"[DEBUG] SQL ERROR AdminUsers: {e}")
        err = "Ошибка базы данных." if lang == "ru" else "Деректер қорында қате."
        return templates.TemplateResponse(
            "admin_login.html",
            {"request": request, "lang": lang, "error": err},
        )

    if not row:
        err = (
            "Неверный логин или пароль администратора."
            if lang == "ru"
            else "Әкімші логині немесе құпиясөзі қате."
        )
        return templates.TemplateResponse(
            "admin_login.html",
            {"request": request, "lang": lang, "error": err},
        )

    return RedirectResponse(url="/admin/dashboard", status_code=302)


@app.get("/admin/logout")
async def admin_logout(request: Request):
    response = RedirectResponse(url="/", status_code=302)
    # если сделаешь авторизацию по кукам — тут будешь чистить cookie
    return response


# ================== АДМИН-ПАНЕЛЬ ===================
@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request)

    # --- фильтры из query-параметров ---
    date_str = request.query_params.get("date")
    group_filter = request.query_params.get("group")

    from datetime import date as _date
    try:
        target_date = _date.fromisoformat(date_str) if date_str else _date.today()
    except ValueError:
        target_date = _date.today()

    if not group_filter or group_filter == "all":
        group_filter = None

    params = {"mark_date": target_date}
    where_extra = ""
    if group_filter:
        where_extra = " AND GroupName = :group_name"
        params["group_name"] = group_filter

    # --- достаём сырые строки из AttendanceMarks ---
    rows_sql = text(f"""
        SELECT LoginName, GroupName, MarkDate, MarkTime, Status
        FROM {ATTENDANCE_TABLE}
        WHERE MarkDate = :mark_date
        {where_extra}
        ORDER BY GroupName, LoginName
    """)
    raw_rows = db.execute(rows_sql, params).fetchall()

    # --- обогащаем данными из таблиц групп (FullName, IsPresent-логика) ---
    view_rows = []
    for r in raw_rows:
        login = r.LoginName
        group_name = r.GroupName
        mark_date = r.MarkDate
        mark_time = getattr(r, "MarkTime", None)
        status_raw = getattr(r, "Status", None)

        # По умолчанию ФИО = логин (если не найдём в группе)
        full_name = login

        table_name = GROUP_TABLES.get(group_name)
        if table_name:
            try:
                full_row = db.execute(
                    text(f"SELECT TOP 1 FullName FROM {table_name} WHERE LoginName = :login"),
                    {"login": login}
                ).fetchone()
                if full_row:
                    # full_row[0] — это FullName
                    full_name = full_row[0]
            except Exception as e:
                print(f"[DEBUG] Error fetching FullName for {login} from {table_name}: {e}")

        # переведём Status в логический IsPresent
        is_present = False
        if isinstance(status_raw, (int, bool)):
            is_present = bool(status_raw)
        elif isinstance(status_raw, str):
            is_present = status_raw.lower() in ("1", "present", "p", "yes", "y", "true")

        view_rows.append({
            "FullName": full_name,
            "LoginName": login,
            "GroupName": group_name,
            "MarkDate": mark_date,
            "MarkTime": mark_time,
            "IsPresent": is_present,
        })

    # --- сводка по группам как раньше (по AttendanceMarks) ---
    summary_sql = text(f"""
        SELECT GroupName, COUNT(*) AS CountPresent
        FROM {ATTENDANCE_TABLE}
        WHERE MarkDate = :mark_date
        {where_extra}
        GROUP BY GroupName
        ORDER BY GroupName
    """)
    summary = db.execute(summary_sql, params).fetchall()

    # список групп для селекта
    group_list = sorted([g for g in GROUP_TABLES.keys() if g != "AdminUsers"])

    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "lang": lang,
            "rows": view_rows,                     # ВАЖНО: теперь rows = view_rows
            "summary": summary,
            "selected_date": target_date.isoformat(),
            "selected_group": group_filter or "all",
            "group_list": group_list,
        },
    )
