from config import config_exists

if config_exists():

    launch()

else:

    print("Setup Required")
