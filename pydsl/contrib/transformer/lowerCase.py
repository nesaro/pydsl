def function(inputdic, inputgt, outputgt):
    palabras = inputdic["input"].string
    return {"output":palabras.lower()}


iclass = "PythonTransformer"
inputdic = {"input":"cstring"}
outputdic = {"output":"cstring"}
