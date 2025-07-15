from url_shortener_service.schema import URLShortener
def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

def get_all_schema():
    return [URLShortener]