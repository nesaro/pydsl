def function(inputdic, inputgt, outputgt):
    if not inputdic["input"]:
        return {}
    numberstr = inputdic["input"]
    number = int(numberstr)
    hexstr = "%X" % number
    return {"output":hexstr}


iclass = "PythonTransformer"
inputdic = {"input":"integer"}
outputdic = {"output":"hex"}
