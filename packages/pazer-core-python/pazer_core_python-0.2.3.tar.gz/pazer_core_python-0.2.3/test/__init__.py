import os

from pazer_core_python import CoreConfig, Core



os.environ["MODE"] = "production"
os.environ["DEBUG"] = "true"
os.environ["LOG_ENABLE"] = "true"

config = CoreConfig()
config.CROSS_ALLOW_CROSS = True


core = Core(config=config,fetch=True)