from myinterpreter import arduinoOrders


done=False

t_DIR = r'ATR|ADL|ADE|AIZ|IZQ|DER|DDE|DIZ'


x=["ATR","ADL","ADE","AIZ","IZQ","DER","DDE","DIZ"]

dirList=["pwm:-100","pwm:100","diagD:-1","diagI:-1","dir:-1","dir:1","diagD:1","diagI:1"]

arduinoOrder=[['Mover', 'ATR']]

def sendData(result):
    pass 


while True:
    if done==False:
        result=[]
        for order in arduinoOrders:
            if order in x:
                result.append(order)
        done=True
        print(result)

    if done==True:
        sendData(result)
        break
    
print("\n--------- Execute Result ---------\n")
print(result)
print("\n")


       
        

        