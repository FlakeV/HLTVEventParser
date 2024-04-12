import os

import dotenv

dotenv.load_dotenv()


class Settings:
    gs_sheet_name = os.getenv('GS_TABLE_NAME')

    retry_count = int(os.getenv('RETRY_COUNT'))
    retry_time = float(os.getenv('RETRY_TIME'))

    json_file_name = os.getenv('JSON_FILE_NAME') + '.json' if '.json' not in os.getenv('JSON_FILE_NAME') else os.getenv('JSON_FILE_NAME')
    json_file_path = os.getenv('JSON_FILE_PATH') if os.getenv('JSON_FILE_PATH')[-1] != '/' else os.getenv('JSON_FILE_PATH')[:-1]
