import os
import time


class Logger:
    @staticmethod
    def isDebug() -> bool:
        return True if os.getenv("DEBUG", None) in [True, "True", "true"] else False

    @staticmethod
    def isMode() -> str:
        return os.getenv("MODE", "NoneMode")

    @staticmethod
    def isLogEnable() -> bool:
        return True if os.getenv("LOG_ENABLE", None) in [True, "True", "true"] else False

    @staticmethod
    def isLogPath() -> str:
        return os.getenv("LOG_PATH", "./Logs/")

    @staticmethod
    def date(timestamp: float | None = None, format: str = "%Y-%m-%d|%H:%M:%S|%Z%z") -> str:
        timestamp = timestamp or time.time()
        return time.strftime(format, time.localtime(timestamp))

    @staticmethod
    def print(msg: str, tag: str = "text", color: str = "white", bold: bool = False) -> None:
        timestamp = Logger.date()
        formatted_msg = f"[{timestamp}] : [{tag.upper()}] : {msg}"
        colored_msg = Logger.text_color(formatted_msg, color)

        if bold:
            colored_msg = Logger.text_bold(colored_msg)

        if Logger.isLogEnable():
            os.makedirs(Logger.isLogPath(), exist_ok=True)
            log_file = os.path.join(
                Logger.isLogPath(),
                f"LOG-{Logger.isMode().upper()}-{Logger.date(timestamp=time.time(), format='%Y%m%d.log')}"
            )
            with open(log_file, "a") as file:
                file.write(f"{formatted_msg}\n")

        if Logger.isDebug():
            print(colored_msg)

    @staticmethod
    def text(msg: str) -> None:
        Logger.print(msg=msg, tag="text", color="reset")

    @staticmethod
    def info(msg: str) -> None:
        Logger.print(msg=msg, tag="info", color="blue")

    @staticmethod
    def debug(msg: str) -> None:
        Logger.print(msg=msg, tag="debug", color="magenta")

    @staticmethod
    def error(msg: str) -> None:
        Logger.print(msg=msg, tag="error", color="red", bold=True)

    @staticmethod
    def warning(msg: str) -> None:
        Logger.print(msg=msg, tag="warning", color="yellow", bold=True)

    @staticmethod
    def critical(msg: str) -> None:
        Logger.print(msg=msg, tag="critical", color="cyan", bold=True)

    @staticmethod
    def system(msg: str) -> None:
        Logger.print(msg=msg, tag="system", color="green", bold=True)

    @staticmethod
    def select(msg: str) -> None:
        Logger.print(msg=msg, tag="select", color="bright_blue", bold=True)

    @staticmethod
    def insert(msg: str) -> None:
        Logger.print(msg=msg, tag="insert", color="bright_green", bold=True)

    @staticmethod
    def update(msg: str) -> None:
        Logger.print(msg=msg, tag="update", color="bright_red", bold=True)

    @staticmethod
    def delete(msg: str) -> None:
        Logger.print(msg=msg, tag="delete", color="bright_black", bold=True)

    @staticmethod
    def text_color(text: str, color: str) -> str:
        colors = {
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
            "reset": "\033[0m",
            "bright_black": "\033[90m",
            "bright_red": "\033[91m",
            "bright_green": "\033[92m",
            "bright_yellow": "\033[93m",
            "bright_blue": "\033[94m",
            "bright_magenta": "\033[95m",
            "bright_cyan": "\033[96m",
            "bright_white": "\033[97m",
        }
        return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"

    @staticmethod
    def text_bold(text: str) -> str:
        return f"\033[1m{text}\033[0m"
