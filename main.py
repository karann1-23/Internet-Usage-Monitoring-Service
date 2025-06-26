from fastapi import FastAPI, Query
from models import SessionLocal, Usage
from sqlalchemy import func,case
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.responses import FileResponse
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI(debug=True)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/top-users")
def top_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    db = SessionLocal()
    now = datetime(2022, 12, 5, 0, 0)  # or any date matching your data
    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    users = db.query(
        Usage.username,
        func.sum(Usage.upload + Usage.download).label("total_usage"),
        func.sum(
            case(
                (Usage.start_time >= day_ago, Usage.upload + Usage.download),
                else_=0
            )
        ).label("usage_last_1d"),
        func.sum(
            case(
                (Usage.start_time >= week_ago, Usage.upload + Usage.download),
                else_=0
            )
        ).label("usage_last_7d"),
        func.sum(
            case(
                (Usage.start_time >= month_ago, Usage.upload + Usage.download),
                else_=0
            )
        ).label("usage_last_30d"),
    ).group_by(Usage.username).order_by(func.sum(Usage.upload + Usage.download).desc())

    total = users.count()
    users = users.offset((page - 1) * page_size).limit(page_size).all()

    db.close()

    result = []
    for user in users:
        result.append({
            "username": user.username,
            "usage_last_1d": user.usage_last_1d,
            "usage_last_7d": user.usage_last_7d,
            "usage_last_30d": user.usage_last_30d,
            "total_usage": user.total_usage
        })

    return {
        "users": result,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@app.get("/")
def root():
    return { "Hello! My name is Karan."}
    

@app.get("/user-details")
def user_details(name: str, timestamp: str):
    print(f"RAW TIMESTAMP RECEIVED: '{timestamp}'")  # For debugging
    db = SessionLocal()
    try:
        ts_clean = timestamp.strip().replace('T', ' ')
        while '  ' in ts_clean:
            ts_clean = ts_clean.replace('  ', ' ')
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d%H:%M:%S"):
            try:
                ts = datetime.strptime(ts_clean, fmt)
                break
            except ValueError:
                ts = None
        if ts is None:
            raise ValueError
    except ValueError:
        db.close()
        raise HTTPException(status_code=400, detail=f"Invalid timestamp format. Use YYYY-MM-DD HH:MM. Got: '{timestamp}'")
    # ... rest of your code ...


    # Find the user
    user_usage = db.query(Usage).filter(Usage.username == name, Usage.start_time <= ts).all()
    if not user_usage:
        db.close()
        raise HTTPException(status_code=404, detail="User not found or no usage before given timestamp.")

    # Calculate usage
    total_upload = sum(u.upload for u in user_usage)
    total_download = sum(u.download for u in user_usage)
    total_usage = total_upload + total_download

    # Last 1, 7, 30 days
    last_1d = ts - timedelta(days=1)
    last_7d = ts - timedelta(days=7)
    last_30d = ts - timedelta(days=30)

    usage_last_1d = sum(u.upload + u.download for u in user_usage if u.start_time >= last_1d)
    usage_last_7d = sum(u.upload + u.download for u in user_usage if u.start_time >= last_7d)
    usage_last_30d = sum(u.upload + u.download for u in user_usage if u.start_time >= last_30d)

    db.close()
    return {
        "username": name,
        "usage_last_1d": usage_last_1d,
        "usage_last_7d": usage_last_7d,
        "usage_last_30d": usage_last_30d,
        "total_usage": total_usage
    }