from cx_Freeze import setup, Executable

setup(
    name="MyApp",
    version="1.0",
    description="My application description",
    executables=[Executable("guiWithFileImput.py")],
)
