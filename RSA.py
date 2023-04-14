# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:44:40 2020

@author: Mr ABBAS-TURKI, Mr Becker Esteban
"""



import hashlib
import binascii

def home_mod_expnoent(x,y,n): #exponentiation modulaire
    """
    param x: int le nombre à élever
    param y: int l'exposant
    param n: int le modulo
    
    return: int le résultat de x^y mod n
    """

    #Nous allons utiliser l'algorithme d'exponentiation modulaire rapide

    carre=x

    resultat=1

    while y>0:

        #afin de ne pas utiliser de la mémoire inutilement nous allons à chaque iteration calculer si y est pair ou impair puis le diviser par 2
        if y%2==1:

            resultat=(resultat*carre) % n

        carre = (carre*carre) % n

        y=y//2

    return resultat

            


def home_ext_euclide(y,b): #algorithme d'euclide étendu pour la recherche de l'exposant secret
    """
    param y: int le premier nombre entier
    param b: int le deuxième nombre entier

    return: int l'exposant secret'
    """

    #Ici nous allons calculer en parallele le pgcd de y et b et la relation de Bezout

    dividend=y
    diviseur=b
    quotient=y//b
    reste=y%b

    #initialisation des variables
    v=[0,1]

    i=0

    while reste!=0:

        i=i+1

        #Il ne faut pas calculer la relation de bezout pour le premier quotient, en effet v0 v1 sont initialisés.
        if i>=1:
            v.append(v[i-1]-quotient*v[i])

        dividend=diviseur
        diviseur=reste
        quotient=dividend//diviseur
        reste=dividend%diviseur
    
    return v[-1]%y

def home_pgcd(a,b): #recherche du pgcd
    if(b==0): 
        return a 
    else: 
        return home_pgcd(b,a%b)

def home_string_to_int(x): # pour transformer un string en int
    z=0
    for i in reversed(range(len(x))):
        z=int(ord(x[i]))*pow(2,(8*i))+z
    return(z)


def home_int_to_string(x): # pour transformer un int en string
    txt=''
    res1=x
    while res1>0:
        res=res1%(pow(2,8))
        res1=(res1-res)//(pow(2,8))
        txt=txt+chr(res)
    return txt




def mot10char(): #entrer le secret
    secret=input("donner un secret de 50 caractères au maximum : ")
    while (len(secret)>51):
        secret=input("c'est beaucoup trop long, 50 caractères S.V.P : ")
    return(secret)
    

#voici les éléments de la clé d'Alice
x1a=3503815992030544427564583819137897895645343456451321234534564646453453456456456456454545458764549189 #p
x2a=3503815992030544427564583819137897895645343456451321234534564646453453456456456456454545642354565471 #q
na=x1a*x2a  #n
phia=((x1a-1)*(x2a-1))//home_pgcd(x1a-1,x2a-1)
ea=17 #exposant public
da=home_ext_euclide(phia,ea) #exposant privé
#voici les éléments de la clé de bob
x1b=4932857219512528676440106034047625505005004262342462342452624255264252574542224462250521525425345743 #p
x2b=9420734535044410552424350537132123002156432123156423112515050515231212312315315123123123154561322453 #q
nb=x1b*x2b # n
phib=((x1b-1)*(x2b-1))//home_pgcd(x1b-1,x2b-1)
eb=23 # exposants public
db=home_ext_euclide(phib,eb) #exposant privé



print("Vous êtes Bob, vous souhaitez envoyer un secret à Alice")
print("voici votre clé publique que tout le monde a le droit de consulter")
print("n =",nb)
print("exposant :",eb)
print("voici votre précieux secret")
print("d =",db)
print("*******************************************************************")
print("Voici aussi la clé publique d'Alice que tout le monde peut conslter")
print("n =",na)
print("exposent :",ea)
print("*******************************************************************")
print("il est temps de lui envoyer votre secret ")
print("*******************************************************************")
x=input("appuyer sur entrer")
secret=mot10char()
print("*******************************************************************")
print("voici la version en nombre décimal de ",secret," : ")
num_sec=home_string_to_int(secret)
print(num_sec)
print("voici le message chiffré avec la publique d'Alice : ")
chif=home_mod_expnoent(num_sec, ea, na)
print(chif)
print("*******************************************************************")
print("On utilise la fonction de hashage sha256 pour obtenir le hash du message",secret)
Bhachis0=hashlib.sha256(secret.encode(encoding='UTF-8',errors='strict')).digest() #sha256 du message
print("voici le hash en nombre décimal ")
Bhachis1=binascii.b2a_uu(Bhachis0)
Bhachis2=Bhachis1.decode() #en string
Bhachis3=home_string_to_int(Bhachis2)
print(Bhachis3)
print("voici la signature avec la clé privée de Bob du hachis")
signe=home_mod_expnoent(Bhachis3, db, nb)
print(signe)
print("*******************************************************************")
print("Bob envoie \n \t 1-le message chiffré avec la clé public d'Alice \n",chif,"\n \t 2-et le hash signé \n",signe)
print("*******************************************************************")
x=input("appuyer sur entrer")
print("*******************************************************************")
print("Alice déchiffre le message chiffré \n",chif,"\nce qui donne ")
dechif=home_int_to_string(home_mod_expnoent(chif, da, na))
print(dechif)
print("*******************************************************************")
print("Alice déchiffre la signature de Bob \n",signe,"\n ce qui donne  en décimal")
designe=home_mod_expnoent(signe, eb, nb)
print(designe)
print("Alice vérifie si elle obtient la même chose avec le hash de ",dechif)
Ahachis0=hashlib.sha256(dechif.encode(encoding='UTF-8',errors='strict')).digest()
Ahachis1=binascii.b2a_uu(Ahachis0)
Ahachis2=Ahachis1.decode()
Ahachis3=home_string_to_int(Ahachis2)
print(Ahachis3%nb)

print("La différence =",Ahachis3%nb-designe)
if (Ahachis3%nb-designe==0):
    print("Alice : Bob m'a envoyé : ",dechif)
else:
    print("oups")