"""
FileLogr: A simple logging utility for Python applications.

Provides a Logger class with methods to configure logging paths, log messages with optional tags and colors, and manage log files.

License: MIT License

GitHub: https://github.com/Futuregus/filelogr

"""

# ~--- Imports ---~
import datetime
import os
import sys
from functools import wraps
# ~----------------------~

# %--- Logger Class ---%

class Logger:

# +--- Class Variables ---+
    _data_dir = None
    _log_file = None
    _configured = False
    _no_console = False
    _default_tag = None
# +----------------------+

# +--- Main Methods ---+

    @classmethod
    def configure(cls, data_dir: str = None, log_file: str = None, no_console: bool = False, default_tag: str = None):
        """
        Configures the logger with the specified data directory and log file name.
        Args:
            - data_dir,: The directory where the log file will be stored. Must be provided.
            - log_file,: The name of the log file (e.g., "app.log"). Must be provided and cannot be an absolute path.
            - no_console,: If True, disables printing log messages to the console. Defaults to False (console output enabled).
            - default_tag,: An optional default tag to prefix all log messages with (e.g., "INFO", "ERROR"). If None, no tag will be added by default.

        Examples:

            `Logger.configure(data_dir="logs", log_file="app.log", no_console=False, default_tag="INFO")`
        """
        if not data_dir or not log_file:
            raise ValueError("Both data_dir and log_file must be provided to configure the logger.")


        if os.path.isabs(log_file):
            raise ValueError("Logger not configured: absolute paths for log_file are not allowed.")

        cls._data_dir = data_dir
        cls._log_file = os.path.join(cls._data_dir, log_file)

        cls._no_console = no_console
        cls._default_tag = default_tag

        os.makedirs(cls._data_dir, exist_ok=True)
        cls._configured = True

    @classmethod
    def log_action(cls, action: str, print_to_console: bool = None, separator: bool = False, tag: str = None, color: str = None):
        """
        Logs an action to the log file.

        Args:
            - action=: The action/message to log.
            - print_to_console=: If True, also prints the message to the console. If None, defaults to the value of no_console from configuration.
            - separator=: If True, logs the message without a timestamp (useful for separators or section headers).
            - tag=: An optional tag to prefix the message with (e.g., "INFO", "ERROR"). If None, uses the default tag from configuration.
            - color=: An optional color name (e.g., "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white") to print the message in the console. Does not affect the log file.

        Examples:

            `Logger.log_action("This is an info message.", tag="INFO", color="green")`

            `Logger.log_action("---This is a separator---", separator=True)`
        """

        if not cls._configured:
            raise Exception("Logger not configured. Please call Logger.configure(data_dir, log_file) before logging actions.")

        if tag is None:
            tag = cls._default_tag

        message = f"[{tag}] {action}" if tag else action

        print_to_console = print_to_console if print_to_console is not None else not cls._no_console

        if print_to_console: # Print the message to the console, with optional color
            if color:
                colors = {
                    "black": "\033[30m",
                    "red": "\033[31m",
                    "green": "\033[32m",
                    "yellow": "\033[33m",
                    "blue": "\033[34m",
                    "magenta": "\033[35m",
                    "cyan": "\033[36m",
                    "white": "\033[37m",
                    "reset": "\033[0m",
                }
                color_code = colors.get(color.lower(), "")
                reset_code = colors["reset"] if color_code else ""
                print(f"{color_code}{message}{reset_code}")
            else:
                print(message)

        try: # Log the message to the file, with or without a timestamp based on the separator flag
            with open(cls._log_file, 'a', encoding='utf-8') as f:
                if separator:
                    f.write(f"{message}\n")
                else:
                    timestamp = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                    f.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            print(f"Logging error: {e}", file=sys.stderr)

    @classmethod
    def log_error(cls, error_message: str):
        """ A convenience method to log error messages with the "ERROR" tag and red color in the console. """
        cls.log_action(error_message, print_to_console=True, tag="ERROR", color="red")

    @classmethod
    def log_warning(cls, warning_message: str):
        """ A convenience method to log warning messages with the "WARNING" tag and yellow color in the console. """
        cls.log_action(warning_message, print_to_console=True, tag="WARNING", color="yellow")

    @classmethod
    def log_info(cls, info_message: str):
        """ A convenience method to log informational messages with the "INFO" tag and blue color in the console. """
        cls.log_action(info_message, print_to_console=True, tag="INFO", color="blue")

    @classmethod
    def log_separator(cls):
        """ a quick way to log a separator line to the log file and console. """
        cls.log_action("----------------------", print_to_console=True, separator=True)

# +----------------------+

# +--- Utility Methods ---+

    @classmethod
    def clear_log(cls):
        """ Clears the log file, then writes a nice '--- Log Cleared ---' entry. """

        try:
            with open(cls._log_file, 'w', encoding='utf-8') as f:
                f.write("")
            cls.log_action("--- Log Cleared ---", separator=False)
        except Exception as e:
            print(f"Clear log error: {e}", file=sys.stderr)

    @classmethod
    def get_log_path(cls):
        """ Returns the full path to the log file. """
        return cls._log_file

    @classmethod
    def get_log_size(cls):
        """Returns the size of the log file in megabytes (MB) rounded to 2 decimal places."""
        MB = 1024 * 1024
        size_mb = round(os.path.getsize(cls._log_file) / MB, 2) if os.path.exists(cls._log_file) else 0.0

        return size_mb

    @classmethod
    def get_log_contents(cls):
        """ Returns the full contents of the log as a list of lines. """

        try:
            with open(cls._log_file, 'r', encoding='utf-8') as f:
                contents = f.read().splitlines()
            return contents
        except Exception as e:
            print(f"Get log contents error: {e}", file=sys.stderr)
            return None

# +----------------------+

# +--- Decorators ---+

    @classmethod
    def catch(cls, method):
        """ A decorator to catch and log exceptions that occur within the decorated method. """
        @wraps(method)
        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except Exception as e:
                cls.log_action(f"Exception in {method.__name__}: {e}", tag="ERROR", color="red")
                raise e
        return wrapper

    @classmethod
    def track(cls, method):
        """ A decorator to log the start and end of the decorated method's execution.  it also logs how long the method took to execute. """
        @wraps(method)
        def wrapper(*args, **kwargs):
            try:
                start_time = datetime.datetime.now()
                cls.log_action(f"Method: {method.__name__} has started.", tag="TRACK", color="cyan")
                result = method(*args, **kwargs)
                end_time = datetime.datetime.now()
                duration = (end_time - start_time).total_seconds()
                cls.log_action(f"Method: {method.__name__} has finished. Duration: {duration:.2f} seconds", tag="TRACK", color="cyan")
                return result
            except Exception as e:
                cls.log_action(f"Error in tracking method: {method.__name__} never finished. Error: {e}", tag="ERROR", color="red")
                raise e

        return wrapper

# %----------------------%


# %----------------------%