import json

def extract_endpoints(swagger_path: str) -> list[str]:
    with open(swagger_path) as f:
        swagger_data = json.load(f)

    # Obtenha os endpoints
    endpoints = ""
    for path, methods in swagger_data.get('paths', {}).items():
        for method in methods.keys():
            endpoints += f"{method.upper()} {path}\n"

    return endpoints