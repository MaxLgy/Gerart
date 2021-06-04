import cv2

plan=cv2.imread("Batiment F rdc 2019-1.png")
plan_resize=cv2.resize(plan,(1300,1000))

class Salle():
    def __init__(self, porte, numero, nom='', dico_nom = [], dico_numero = [] ): # salle avec un numero et un personnel assigné
        self.__porte = porte #liste de pixel
        if dico_nom!=[]:
            self.nom = self.nom(nom,dico_nom)
        else:
            self.nom = nom

        if dico_numero!=[]:
            self.__numero = self.numero(numero,dico_numero)
        else:
            self.__numero = numero

    def __str__(self):
        if len(self.nom)==0:
            return 'Salle '+self.__numero+' -- non assignée'
        return 'Salle '+self.__numero+' -- '+self.nom


    def numero(self,num,d_num):
        if num not in d_num:
            return "numéro inconnu"
        else: return num

    def nom(self,nom,d_nom):
        if nom not in d_nom:
            return "nom inconnu"
        else: return nom


if __name__=='__main__':
    S = Salle([None],'E006','Zerr')
    print(S)
    cv2.imshow("Output2", plan_resize)
    cv2.waitKey(0)
