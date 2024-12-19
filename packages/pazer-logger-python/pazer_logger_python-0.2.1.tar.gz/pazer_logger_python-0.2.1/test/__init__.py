import os

from pazer_logger_python import Logger


os.environ["ENV"] = "production"
os.environ["DEBUG"] = "true"
os.environ["LOG_ENABLE"] = "true"
logs = Logger()
logs.system("HI")