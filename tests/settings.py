import dotenv


dotenv.load_dotenv('.env')  # Local overrides (not tracked)
dotenv.load_dotenv('.env_defaults')  # Development defaults (tracked)


from ladder.settings import *  # NOQA


SILENCED_SYSTEM_CHECKS = tuple()
