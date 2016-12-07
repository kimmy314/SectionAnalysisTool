pyinstaller --noconsole --icon=icon.ico SectionAnalysisTool.py
xcopy /Y "%CD%\icon.ico" "%CD%\dist\SectionAnalysisTool\icon.ico"