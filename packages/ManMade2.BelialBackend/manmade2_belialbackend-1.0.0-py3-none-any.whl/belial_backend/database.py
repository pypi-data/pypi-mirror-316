from pathlib import Path
from belial_db import create_connection
from belial_db.repos import MapRepo, AssetRepo

output_path = Path("C:/Users/MadsKris/Desktop/Converted Data")
DATABASE_URL = f"sqlite:///{output_path}/data.db"
engine = create_connection(DATABASE_URL, echo=False)
map_repository = MapRepo(engine)
asset_repository = AssetRepo(engine)


def create_map_repo() -> MapRepo:
    return map_repository


def create_asset_repo() -> AssetRepo:
    return asset_repository
