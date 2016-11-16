pyinstaller --noconsole --icon=icon.ico SectionAnalysisTool.py
copy /Y %CD%\SectionAnalysisToolCopy.spec %CD%\SectionAnalysisTool.spec
pyinstaller SectionAnalysisTool.spec