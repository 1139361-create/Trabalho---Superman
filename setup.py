# pip install cx_freeze
import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(
                   script="main.py", 
                   icon="base/icone.ico",
                    target_name="SuperMan.exe"
                   ) ]
cx_Freeze.setup(
    name = "Super Man",
    options={
        "build_exe":{
            "packages":["pygame"],
            "include_files":["base","recursos"]
        }
    }, executables = executaveis
)

# python setup.py build
# python setup.py bdist_msi