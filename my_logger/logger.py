from datetime import datetime


class Logger:
    def log(self, message: str) -> str:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return f'{str(dt)} | {message}'


class ConsoleLogger(Logger):
    def log(self, message: str) -> str:
        message = Logger.log(self, message)
        print(message)
        return message


class FileLogger(Logger):
    def __init__(self, file_name):
        self.file_name = file_name

    def log(self, message: str) -> str:
        message = Logger.log(self, message)
        with open(self.file_name, 'a') as file:
            file.write(message)
        return message
