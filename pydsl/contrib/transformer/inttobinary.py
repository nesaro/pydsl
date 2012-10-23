def function(inputdic, inputgt, outputgt):
    if inputdic["input"].string == "": 
        return {}
    numberstr = inputdic["input"].string
    number = int(numberstr)
    binstr = str(bin(number))[2:]
    return {"output":binstr}


iclass = "PythonTransformer"
inputdic = {"input":"integer"}
outputdic = {"output":"binary"}
