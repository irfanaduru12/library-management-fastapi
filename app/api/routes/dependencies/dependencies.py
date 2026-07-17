from fastapi import Query

def pagination_params(skip: int = Query(0, ge=0, description="Records to be skipped"),
               limit: int = Query(10, ge=1, description="Max records to be shown")):
    safe_limit = min(limit, 100)

    return {"skip": skip, "limit": safe_limit}