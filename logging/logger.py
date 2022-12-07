from datetime import datetime


class Logger:
    def log(self, message: str) -> str:
        dt = datetime.now()
        return str(dt).join(f'| {message}')


class ConsoleLogger(Logger):
    def log(self, message: str) -> str:
        message = Logger.log(message)
        print(message)
        return message


class FileLogger(Logger):
    def __init__(self, file_name):
        self.file_name = file_name

    def log(self, message: str) -> str:
        message = Logger.log(message)
        with open(self.file_name, 'a') as file:
            file.write(message)
        return message
