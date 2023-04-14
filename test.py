def home_ext_euclide(y,b): #algorithme d'euclide étendu pour la recherche de l'exposant secret
    """
    param y: int le premier nombre entier
    param b: int le deuxième nombre entier

    return: int le résultat de de la relation de Bezout
    """

    #Ici nous allons calculer en parallele le pgcd de y et b et la relation de Bezout

    dividend=y
    diviseur=b
    quotient=y//b
    reste=y%b

    #initialisation des variables
    u=[1,0]

    v=[0,1]

    i=0

    while reste!=0:

        i=i+1

        if i>=1:
                
            u.append(u[i-1]-quotient*u[i])
    
            v.append(v[i-1]-quotient*v[i])

        dividend=diviseur
        diviseur=reste
        quotient=dividend//diviseur
        reste=dividend%diviseur
    
    return u[-1],v[-1]

print(home_ext_euclide(280,11))