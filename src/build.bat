pyinstaller --noconsole --icon=icon.ico SectionAnalysisTool.py
xcopy /Y "%CD%\SectionAnalysisToolCopy.spec" "%CD%\SectionAnalysisTool.spec"
pyinstaller SectionAnalysisTool.spec