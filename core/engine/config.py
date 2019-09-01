import yaml
try:
    conf_file = yaml.load(open('app-config.yml'), Loader=yaml.FullLoader)
    # conf_file = yaml.load(open('app-config.yml'))
except:
    conf_file = {}

DB_CONF = {
    'dbname': conf_file.get('storage_sqlite', {}).get('dbname', '')
}

# 1: logging.CRITICAL,
# 2: logging.ERROR,
# 3: logging.WARNING,
# 4: logging.INFO,
# 5: logging.DEBUG
DEBUG_LEVEL = conf_file.get('debug_level', 3)
