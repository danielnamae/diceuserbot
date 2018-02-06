import requests
import datetime
import random
import MySQLdb
import telegram

token=""

class dbConn:

    ### Database settings ###
    dsn = ("localhost", "botuser" , "b0tus3r." , "akelarre")

    def __init__(self):
        self.conn = MySQLdb.connect(*self.dsn)
        self.cur = self.conn.cursor()        
    
    def cierre(self):
        db.close()
        
    def __enter__(self):
        return self
        
    def insertar(self):
    
        sql = """INSERT INTO eventos (reino, descripcion) VALUES ('Castilla','Tres bandidos aparecen en medio del camino')"""
         
        try:
        
            self.cur.execute(sql)
            self.conn.commit()
        except:
            print ("Error en la insercion")
            self.conn.rollback()
         

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=20):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text, parse):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': parse}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()
        
        print ("Tamano de get_result: " + str(len(get_result)))
        
        if len(get_result) > 0:
            last_update = get_result[-1]
            return last_update
            
        else:
            try:
                return 0
            except IndexError:
                main()

        

dice_bot = BotHandler(token)
dados = ['3','4','6','8','10','12','20','100']


def dados(dad,num):
    if num > 0: 
        cont=0   
        while num > cont:
            res = res + random.randint(1,dad)
            cont = cont + 1
    return res

def comprueba(dad):
    if dad in dados:
        return True

dados = ['2','3','4','6','8','10','12','20','100']

def fdados(dad,num,suma):
    print ("Suma vale" + str(suma))
    if int(num) > 0:              
        cont = 0
        res = 0
        dad = int(dad)        
        acumula = ""        
        while int(num) > cont:
            tir = random.randint(1,dad)    
            res = res + tir
            if acumula == "":
                acumula = str(tir) + "  "
            else:
                acumula = acumula + str(tir) + "  "
            cont = cont + 1

        if suma != '0':
            res = res + suma
            res = "<b>" + str(res) + "</b>"
            acumula = res + " [ " + acumula + "]" + " + " + str(suma)
        
        else:
            res = res
            res = "<b>" + str(res) + "</b>"
            acumula = res + " [ " + acumula + "]"
        
    return(acumula)

def comprueba(dad):
    if dad in dados:
        return True
    else:    
        return False

def seleccionaMej(array,num):

    array.sort()
    tam = len(array)
    for i in range(len(array)):
         print (array[i])

    devuelveArray = []
    devuelveArrayPeor = []
    ini = tam - num

    
    for i in range(ini,tam):    
        devuelveArray.append(array[i])
    
    for i in range(0,ini):
        devuelveArrayPeor.append(array[i])

    return devuelveArray, devuelveArrayPeor


def fdadosext(num,dad,besth):

    almacenDados = []
    besth = int(besth)
    num = int(num)
    if besth > 0 and besth >= num:
        almacenDados = [-1, "Ha elegido un numero de dados 'h' mayor o igual que las tiradas"]
        almacenDadosReverse = [-1, "Ha elegido un numero de dados 'h' mayor o igual que las tiradas"]

    elif besth <= 0:
        almacenDados = [-1, "Ha elegido un numero de dados 'h' igual o menor que 0"]
        almacenDadosReverse = [-1, "Ha elegido un numero de dados 'h' igual o menor que 0"]
    else:

        if int(num) > 0:
            cont = 0
            res = 0           
            while int(num) > cont:
                res = random.randint(1,int(dad))
                print("Tirada " + str(cont) + ":" + str(res))
                almacenDados.append(res)
                cont = cont + 1

            if (besth > 0) and (besth < num):
                almacenDados, almacenDadosReverse = seleccionaMej(almacenDados,besth)                

            
        else:
            almacenDados = [-1, "Ha elegido un numero de tiradas incorrecto"]
            almacenDadosReverse = [-1, "Ha elegido un numero de tiradas incorrecto"]        
            
    return almacenDados, almacenDadosReverse

   
        
#######################################################
      

def main():
    print("Inicializando el Bot")
    new_offset = None
    
    dbs = dbConn()
    dbs.insertar()

    while True:
        print("Activando el bucle principal")
        dice_bot.get_updates(new_offset)

        last_update = dice_bot.get_last_update()
        print ("Estado actual: " + str(last_update))
        NoUpdate = isinstance(last_update, int)
        print("NoUpdate: " + str(NoUpdate))
        last_edited = 1
     
        if NoUpdate is False:
            
            try:
                last_update_id = last_update['update_id']
                last_chat_text = last_update['message']['text']
                last_chat_id = last_update['message']['chat']['id']
                last_chat_name = last_update['message']['chat']['first_name']
                
                
            except KeyError:
                print("Error en el procesamiento del last update")
            
            try:
                last_edited = last_update['edited_message']['from']['id']
                print ("Last edited --> " + str(last_edited))
                
            except KeyError:
                last_edited = 0
                
            ### Si es un mensaje editado, nos olvidamos
            if last_edited > 0:
                print ("Mensaje editado, no se procesa")
                new_offset = last_update_id + 1
                      
            else:
                print (last_edited)
                ### Comprobar si es un usuario directamente
                if 'last_chat_name' in locals():
                    user = last_chat_name
                 
                ### De lo contrario se usa un grupo
                else:
                    try:                
                        user = last_update['message']['from']['first_name']
                        
                    except KeyError:
                        print("Error en el asignamiento de usuario")
                        main()
                              
                dicepet = last_chat_text.lower()
                new_offset = last_update_id + 1
               
                if '/ayuda' in dicepet:
                    dice_bot.send_message(last_chat_id, "<b>Dados disponibles</b>: 'd2,d3,d4,d6,d8,d10,d12,d20 y d100'. Uso: numero de dados mas tipo de dados unidos por la letra 'd'. Ejemplos: 1d10, 3d100, 2d8. Si queremos escoger los resultados más altos, usar 'h'. Ejemplos: 4d6h3, escoge los tres resultados más altos.",telegram.ParseMode.HTML)
                    
                else:
                
                    if dicepet.startswith("/") is True:
                        dicepet = dicepet.strip('/')
                    
                    if '@diceuserbot' in dicepet:
                        pos = dicepet.index('@')
                        dicepet = dicepet[0:pos]
                    
                    if 'd' in dicepet:
                        pos = dicepet.index('d')
                        idx = dicepet[0:pos]
                        tdad = (dicepet[pos:]).strip('d')
                        hsi = 0
                        suma = 0

                        if '+' in tdad:
                            pos = tdad.index('+')                            
                            suma = (tdad[pos:]).strip('+')
                            suma = int(suma)
                            tdad = tdad[0:pos]                          
                            hsi = 2

                        if 'h' in tdad:
                            pos = tdad.index('h')                            
                            hbest = (tdad[pos:]).strip('h')
                            hbest = int(hbest)
                            tdad = tdad[0:pos]                          
                            hsi = 1

                        rest = comprueba(tdad)
                        
                        
                        if rest is True and int(idx) and hsi == 0:                                                       
                            res = fdados(tdad,idx,suma)
                            res = "<b>" + str(user) + "</b> " + "<i>" + str(dicepet) + "</i> " + "--> " + str(res)
                            dice_bot.send_message(last_chat_id, 'Resultado de tirar {}'.format(res),telegram.ParseMode.HTML)

                        elif rest is True and int(idx) and hsi == 2:                                                       
                            res = fdados(tdad,idx,suma)
                            res = "<b>" + str(user) + "</b> " + "<i>" + str(dicepet) + "</i> " + "--> " + str(res)
                            dice_bot.send_message(last_chat_id, 'Resultado de tirar {}'.format(res),telegram.ParseMode.HTML)

                        elif rest is True and int(idx) and hsi == 1:                                                       
                            if hbest > 0:                                
                                resArray, resArrayPeor = fdadosext(idx,tdad,hbest)                                
                            
                                
                                if resArray[0] > -1:
                                    tiradas = "[ "
                                    gb = 0
                                    for h in range(len(resArrayPeor)):                                        
                                        tiradas = tiradas + str(resArrayPeor[h]) + " "

                                    for j in range(len(resArray)):
                                        gb = gb + resArray[j]
                                        tiradas = tiradas + "<i>" + str(resArray[j]) + "</i>" + " "
                                        
                                    tiradas = tiradas + " ]"
                                    res = "<b>" + str(user) + "</b> " + "<i>" + str(dicepet) + "</i> " + "--> " + "<b>" + str(gb) + "</b> " + tiradas
                                    dice_bot.send_message(last_chat_id, 'Resultado de tirar {}'.format(res),telegram.ParseMode.HTML)  
                            
                            else:
                                dice_bot.send_message(last_chat_id, "<b>Incorrecto</b>. Uso: '2d20h1, 3d10h2, etc'",telegram.ParseMode.HTML)                                        
                                
                        else:
                            dice_bot.send_message(last_chat_id, "<b>Incorrecto</b>. Dados disponibles: 'd2,d3,d4,d6,d8,d10,d12,d20 y d100'",telegram.ParseMode.HTML)
                    
                    else:
                        dice_bot.send_message(last_chat_id, "<b>Incorrecto</b>. Uso: '1d20, 3d10, etc'",telegram.ParseMode.HTML)

        else:
            print ("No hay cambios")
    
	
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
