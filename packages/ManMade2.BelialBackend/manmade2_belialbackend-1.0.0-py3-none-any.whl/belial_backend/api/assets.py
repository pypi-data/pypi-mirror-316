import json
from pathlib import Path

from flask import Blueprint, Response, jsonify

from belial_backend.database import create_map_repo, create_asset_repo
from belial_backend.schemas import AssetSchema

assets_blueprint = Blueprint("assets", __name__)
assets_path = Path("C:/Users/MadsKris/Desktop/Converted Data")
maps_path = assets_path / "maps"
map_repo = create_map_repo()
asset_repo = create_asset_repo()


@assets_blueprint.route("/assets/<map_id>", methods=["GET"])
def get_map_assets(map_id: int) -> tuple[Response, int]:
    """Retrieve assets for a given map ID with a database timeout.

    Args:
        map_id (int): The ID of the map.

    Returns:
        tuple: JSON response with assets or error message.
    """

    print(f"Getting assets for map {map_id}")

    try:
        map_instance = map_repo.get_map(map_id)  # Added database timeout of 30 seconds
    except TimeoutError:
        return jsonify({"error": "Database operation timed out"}), 503

    if map_instance is None:
        return jsonify({"error": f"Map with id {map_id} not found"}), 404

    if len(map_instance.assets) == 0:
        return jsonify({"error": f"Map with id {map_id} has no assets"}), 404

    assets: list[AssetSchema] = []

    for asset in map_instance.assets:
        assets.append(AssetSchema.model_validate(asset))

    return jsonify(assets), 200


@assets_blueprint.route("/map/<name>", methods=["GET"])
def get_map(name: str) -> tuple[Response, int]:

    try:
        with open(maps_path / f"{name}.json", "r") as file:
            model_data = json.load(file)
            return jsonify(model_data), 200

    except FileNotFoundError:
        return jsonify({"error": f"{maps_path}/{name}.json not found"}), 404

    except json.JSONDecodeError:
        return jsonify({"error": f"{maps_path}/{name}.json is not valid JSON"}), 400

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


# region old code
# @assets_blueprint.route("/assets/map/<id>", methods=["GET"])
# def get_map_assets(id: int):
#     map = map_repo.get_map(id)

#     if map is None:
#         return jsonify({"error": f"Map with id {id} not found"}), 404

#     with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
#         with zipfile.ZipFile(temp_zip, "w") as zip_file:
#             for asset_file in map.AssetFiles:
#                 zip_file.write(f"{assets_path}\\{asset_file.Path}", Path(str(asset_file.Path)).name)

#         temp_zip_path = temp_zip.name

#     return send_from_directory(
#         directory=os.path.dirname(temp_zip_path),
#         path=os.path.basename(temp_zip_path),
#         as_attachment=True,
#         download_name="maps.zip",
#         mimetype="application/zip",
#     )
# endregion
