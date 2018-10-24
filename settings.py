try:
    from _settings import *
except ImportError:
    # put default settings here
    LOCAL_DATA_DIR = 'local_data/'