@echo off
if "%1" == "html" (
    poetry run sphinx-build -b html . _build/html
)
