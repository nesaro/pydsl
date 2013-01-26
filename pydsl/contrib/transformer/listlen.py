def function(inputdic, inputgt, outputgt):
    liststr = inputdic["input"]
    return {"output":liststr.count(",") + 1}


iclass = "PythonTransformer"
inputdic = {"input":"list"}
outputdic = {"output":"integer"}
