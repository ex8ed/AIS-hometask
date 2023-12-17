from pathlib import Path
import json

all_languages = {file.stem: json.loads(file.absolute().read_text()) for file in Path("config/internationalization/languages").iterdir()}
