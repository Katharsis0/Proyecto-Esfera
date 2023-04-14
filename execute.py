from myinterpreter import arduinoOrders


done=False

dirList=["pwm:-100","pwm:100","diagD:-1","diagI:-1","dir:-1","dir:1","diagD:1","diagI:1"]



def sendData(result):
    pass 


while True:
    if not done:
        for order in arduinoOrders:
            result= []
            if order in dirList:
                result.append(order)
        done=True
    if done:
        sendData(result)


       
        

        