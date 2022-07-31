title RQ Worker
call venv\Scripts\activate.bat
rq worker --with-scheduler -w rq_win.WindowsWorker
pause