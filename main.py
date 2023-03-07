import tkinter
import serial

janela = tkinter.Tk()

janela.geometry()

ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

if ser.isOpen():
    print('Porta aberta')

sem = ""
com = ""
var_sem = []
var_com = []

read_limit = 3000


def capt_sem():
    global var_sem
    var_sem = redux(capture(read_limit))


def capt_com():
    global var_com
    var_com = redux(capture(read_limit))


def dell_sem():
    rec_sem.delete('1.0', tkinter.END)
    return


def dell_com():
    rec_com.delete('1.0', tkinter.END)
    return


def comp():
    print(isole(var_sem,var_com)[1])
    return


def isole(csem,ccom): #compara itens (IDS)
    #print(csem)
    #print(ccom)
    vcom = []
    ambos = []

    for i in range(len(ccom[1])):
        for j in range(len(csem[1])):
            if ccom[1][i] == csem[1][j]:
                ambos.append(ccom[1][i])

    for i in range(len(ccom[1])):
        contem = False

        for j in range(len(ambos)):
            if ccom[1][i] == ambos[j]:
                contem = True


        if not contem:
            vcom.append(ccom[1][i])

    return [ambos, vcom]


def redux(carray): #Exporta um vetor com os ids e n de vezes que apareceu
    vector = carray
    nxvector = []
    outvector = []

    carrayend = True
    while carrayend:
        nvector = []
        nx = 0

        for i in range(len(vector)):
            if vector[0][0] == vector[i][0]:
                nx += 1
            else:
                nvector.append(vector[i])

        nxvector.append(nx)
        outvector.append(vector[0][0])
        vector = nvector

        if len(vector) == 0:
            carrayend = False



    return [nxvector, outvector]



def capture(n): #Captura os dados da porta serial
    ser_data = ""
    i_0 = 0
    can_sem = []
    while ser.isOpen():
        data = str(ser.readline())
        ser_data += data
        i_0 += 1
        can_sem.append(split(data))

        if i_0 >= n:
            break
    #print(can_sem)
    return can_sem


def split(data): #Separa os dados por mensagem
    out_data = []
    indata = []
    datstr = ""
    zind = 0
    junp = 0
    for i in range(len(data)):
        if junp > 0:
            junp -=1
            continue
        if data[i] == "/":
            if data[i + 1] == "I":
                datstr = ""
                ind = 1
                junp += 1
                continue
            if data[i + 1] == "O":
                indata.append(datstr)
                datstr = ""
                ind = 2
                junp += 1
                continue
            if data[i + 1] == "H":
                indata.append(datstr)
                datstr = ""
                junp += 1
                continue
        if data[i] == "\\" and data[i+1] == "n":
            zind += 1
            out_data = indata
            ind = 0
            junp += 2
            continue

        if data[i] == "\\" and data[i+1] == "r":
            junp += 1
            continue

        if data[i] == "b" and data[i+1] == "\'":
            junp += 1
            indata = []
            continue

        datstr += data[i]

    return out_data


gravar_sem = tkinter.Button(janela, text='Gravar Sem', command=capt_sem)
#del_sem = tkinter.Button(janela, text='Deletar Sem', command=dell_sem)
#list_sem = tkinter.Text(janela, width=70, height=12)
#list_sem.pack(side='bottom')


gravar_com = tkinter.Button(janela, text='Gravar Com', command=capt_com)
#del_com = tkinter.Button(janela, text='Deletar Com', command=dell_com)
#list_com = tkinter.Text(janela, width=70, height=12)
#list_com.pack(side='bottom')


compare = tkinter.Button(janela, text='Comparar', command=comp)


# posicionando os botoes
gravar_sem.pack(side='left')
gravar_com.pack(side='right')

#del_sem.pack(side='left')
#del_com.pack(side='right')

compare.pack(side='top')

# mostrar janela
janela.mainloop()

ser.close()