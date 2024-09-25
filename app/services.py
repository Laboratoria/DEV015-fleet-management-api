from app.models import taxi

def fetch_taxis(plate=None, page=1, limit=10):
    query = taxi.query
    if plate:
        query = query.filter(taxi.plate.ilike(f'%{plate}%'))
    
    total_taxis = query.count()
    taxis = query.offset((page - 1) * limit).limit(limit).all()
    return {
        "taxis": [{"id": taxi.id, "plate": taxi.plate} for taxi in taxis],
        "total": total_taxis
    }