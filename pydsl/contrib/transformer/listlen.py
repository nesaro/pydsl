def function(inputdic, inputgt, outputgt):
    liststr = inputdic["input"]
    return {"output":liststr.count(",")}


iclass = "PythonTransformer"
inputdic = {"input":"list"}
outputdic = {"output":"integer"}
