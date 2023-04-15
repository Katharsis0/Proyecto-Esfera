#from myinterpreter import arduinoOrders




arduinoOrders=['ATR','ADL','ATR','Led','Circulo','Led','Trompo']

def sendData(result):
    pass 
done=False
result=[]

while True:
    if done==False:
        for order in arduinoOrders:
            if order == 'ADL':
                result.append("pwm:100;")
            if order == 'ATR':
                result.append("pwm:-100;")
            if order == 'DER':
                result.append("dir:1;")
            if order == 'IZQ':
                    result.append("dir:-1;")
            if order == 'DDE':
                    result.append("diagD:1;")
            if order == 'DIZ':
                    result.append("diagI:1;")
            if order == 'ADE':
                    result.append("diagD:-1")
            if order == 'AIZ':
                    result.append("diagI:-1;")
            if order == 'Led':
                    result.append("led;")
            if order == 'Trompo':
                    result.append("trompo;")
            if order == 'Circulo':
                    result.append("circulo;")
        done=True

    if done==True:
        #sendData(result)
        break
    
print("\n--------- Execute Result ---------\n")
print(result)
print("\n")


       
        

        