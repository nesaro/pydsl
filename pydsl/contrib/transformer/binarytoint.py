def function(inputdic, inputgt, outputgt):
    if inputdic["input"].string == "": 
        return {}
    numberstr = inputdic["input"].string
    decimalnumber = int(numberstr, 2)
    decimalstr = str(decimalnumber)
    return {"output":decimalstr}


iclass = "PythonTransformer"
inputdic = {"input":"binary"}
outputdic = {"output":"integer"}
