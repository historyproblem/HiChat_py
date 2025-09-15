import sys
import asyncio
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop
from app.windows.MainWindow import HiChatWindow
from core.ORM import AsyncORM

def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    win = HiChatWindow()
    win.show()

    with loop:
        loop.create_task(AsyncORM.create_all())
        loop.run_forever()

if __name__ == "__main__":
    main()
