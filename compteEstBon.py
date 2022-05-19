from random import sample, randint
from itertools import combinations
from copy import copy
import time

tokens = [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,25,50,75,100]
tokensIndex = range(len(tokens))
tokensIndexDraw = sample(tokensIndex, 6)  # passer par les index et sample pour éviter des doublons de random.choices
drawTokens = [tokens[index] for index in tokensIndexDraw]  # liste des 6 plaques retenues

target = randint(101,999)   # tirage de la valeur à calculer avec les tokens tirés

distance = 999
counter = 0  #pour comptabiliser le nombre d'opérations effectuées

bestSolution = []
exactSolutions = []



# fonctions opérations ; dans la mesure où les nombres n1 et n2 sont triés (n1<=n2)
# inutile d'utiliser des valeurs absolues ou des min, max
# la multiplication n'a pas lieu si n1 = 2 et n2 = 2 car alors n1+n2=n1*n2
# la soustraction n'a pas lieu si n1 = n2 (pour ne pas renvoyer zéro)
# la division n'a pas lieu si n1 = 1 (car la multiplication donne le même résultat), si n1 = 2 et n2 = 4 car alors n2-n1 = n2/n1
# la division n'a pas lieu si n2 % n1 != 0 (on n'admet que les entiers)

def addNumbers(n1, n2):
    return [n1 + n2, "{} + {} = {}".format(n1, n2, n2+n1)]

def multNumbers(n1, n2): 
    if n1 == 2 and n2 == 2:
        return None
    else:
        return [n1 * n2, "{} x {} = {}".format(n1, n2, n2*n1)]

def subNumbers(n1, n2):
    if n1 == n2:
        return None        
    else:
        return [n2 - n1, "{} - {} = {}".format(n2, n1, n2-n1)]

def divNumbers(n1, n2):
    if n1 == 1 or (n1 == 2 and n2 == 4) or n2 % n1 != 0:
        return None        
    else:
        return [int(n2 / n1), "{} / {} = {}".format(n2, n1, int(n2/n1))]

class Panel:
    """Dans cette classe, numbers est une liste de nombres : soit plaque initiale, soit nombre calculé
    Way est la suite des calculs effectués pour obtenir les nombres de numbers"""
    def __init__(self, numbers, way):
        self.numbers = numbers
        self.way = way
    
    # fonction créant les permutations de nombres 2 à 2
    # tri des permuations (n1, n2) avec n1 <= n2
    # élimination des doublons
    # ajout des nombres non utilisés dans la permutation ; ajout des chemins ; reconstitution de Panel()
    # les siblings sont les permutations par 2 des nombres d'un panel
    # pour un panel de nombres donnés par exemple [5,25,6,32] va renvoyer ; [5,25,6,32], [5,6,25,32], [5,32,25,6],[25,6,32,5], [25,32,6,5], [6,32,5,25]. Elimine les doublons.
    def siblings(self):
        siblings = []
        panelSiblings = []
        if len(self.numbers) > 1:
            combos = combinations(self.numbers, 2)
            combos = [sorted(tup) for tup in combos]  # classe les nombres par ordre croissant ; renvoie une liste de listes à deux éléments
            combos = [tuple(tup) for tup in combos]  # nécessité de transformer les listes à deux éléments en tuple pour pouvoir faire set : problème de hashage
            combos = list(set(combos))              # set permet d'éliminer les doublons

            for combo in combos:
                brotherCopy = copy(self.numbers)
                brotherCopy.remove(combo[0])
                brotherCopy.remove(combo[1])
                sibling = list(combo)
                sibling.extend(brotherCopy)
                
                siblings.append(sibling) 
                
        ways = [self.way] * len(siblings)
        siblings = list(zip(siblings, ways))

        for sibling in siblings:
            panel = Panel(sibling[0], sibling[1])
            panelSiblings.append(panel)

        return panelSiblings   

    # à partir d'un Panel, création des enfants
    # addition, multiplication, soustraction, division des deux premiers nombres
    # reconstitution de Panel à partir du nouveau nombre calculé, des nombes restants, du chemin des opérations
    # les opération interdites (retour None) ne sont pas ajoutées dans children
    # les children sont issus des opérations sur les deux premiers nombres d'un panel
    # par exemple : [5,25,6,32] donnera [30,6,32], [125,6,32], [20,6,32], [5,6,32]
    # on ne fait de divisions que si elles sont entières. Pas de soustraction si les deux nombre sont égaux, pour éviter des zéros

    def children(self):
        children = []
        addChild = addNumbers(self.numbers[0], self.numbers[1])
        multChild = multNumbers(self.numbers[0], self.numbers[1])
        subChild = subNumbers(self.numbers[0], self.numbers[1])
        divChild = divNumbers(self.numbers[0], self.numbers[1])

        # création des arrays de nombre et des strings qui vont créer les Panel child
        # création de children
        
        
        numbersAdd = [addChild[0]]
        numbersAdd.extend(self.numbers[2:])
        wayAdd = "{}\n{}".format(self.way, addChild[1])
        panelAdd = Panel(numbersAdd, wayAdd)
        children.append(panelAdd)

        if multChild is not None:
            numbersMult = [multChild[0]]
            numbersMult.extend(self.numbers[2:])
            wayMult = "{}\n{}".format(self.way, multChild[1])
            panelMult = Panel(numbersMult, wayMult)
            children.append(panelMult)
        else:
            pass

        if subChild is not None:
            numbersSub = [subChild[0]]            
            numbersSub.extend(self.numbers[2:])
            waySub = "{}\n{}".format(self.way, subChild[1])
            panelSub = Panel(numbersSub, waySub)
            children.append(panelSub)
        else:
            pass
        
        if divChild is not None:
            numbersDiv = [divChild[0]]            
            numbersDiv.extend(self.numbers[2:])
            wayDiv = "{}\n{}".format(self.way, divChild[1])
            panelDiv = Panel(numbersDiv, wayDiv)
            children.append(panelDiv)
        else:
            pass

        return children   


    # stockage des solutions
    def stockSolution(self):
        global distance
        global bestSolution 
        global exactSolutions
        global timeFirst
        
        result = self.numbers[0]

        if abs(result - target) < distance and (result - target) != 0:
            distance = abs(result - target)
            bestSolution = [result, self.way]
            timeFirst = time.time()
        elif result - target == 0:
            if distance > 0:
                timeFirst = time.time()
                distance = 0
            solution = [result, self.way]
            exactSolutions.append(solution)       
        else:
            pass
        
        return bestSolution, exactSolutions

    # diverses impressions : cible, tirage, solutions, temps écoulé...
    def printResults(self, start, end, first):
        print(f'valeur cible : {target} --- plaques : {numbers}')
        print(f'{counter} solutions testées en {end - start} secondes')

        if distance == 0:
            solutions = self.stockSolution()[1]
            firstSolution = solutions[0]
            firstSolPanel = Panel(firstSolution[0], firstSolution[1])
            print(f'il existe au moins une solution exacte : {firstSolPanel.numbers}{firstSolPanel.way}')
            
            #notation pour avoir des millisecondes lisibles ; voir https://stackoverflow.com/questions/658763/how-to-suppress-scientific-notation-when-printing-float-values
            print(f'première solution exacte trouvée en {((first - start)/1000):.20f} millisecondes')
   
            print(f'nombre de solutions exactes testées : {len(solutions)}')
            
        else:
            solution = self.stockSolution()[0]
            bestSolPanel = Panel(solution[0], solution[1])
            print(f'pas de solution exacte\nmeilleure solution = {bestSolPanel.numbers}{bestSolPanel.way}')
            print(f'écart avec la valeur cible = {distance}\nvaleur trouvée en {first - start} secondes')


# lancement de l'algorithme ; boucle de fonction récursive
def findSolution(panel):
    global counter
    siblings = panel.siblings()
    for sibling in siblings:
        if len(sibling.numbers) > 1:
            children = sibling.children()
            for child in children:
                counter += 1
                child.stockSolution()
                findSolution(child)
        else:
            pass


#Exemples pour tester. Soit on impose les plaques, soit on les tire au sort. Idem pour la valeur cible.
numbers = [1,75,3,100,2,10,7]
#numbers = drawTokens
target = 620
#target = target
way = ""
panel = Panel(numbers, way)
timeStart = time.time()
findSolution(panel)
timeEnd = time.time()
panel.printResults(start=timeStart, end=timeEnd, first=timeFirst)
