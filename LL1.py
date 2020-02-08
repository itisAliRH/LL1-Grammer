grammer = list()

print('Enter grammer:')
inputGrammer = input().split('->')
i = 1

while(inputGrammer[0] != '*'):
    if 64 < ord(inputGrammer[0]) < 91:
        grammer.append(tuple((inputGrammer[0],inputGrammer[1],i)))
        i+=1
    else:
        print('{} is not valid!'.format(inputGrammer[0]))
    print('Enter grammer or \'*\' for finish:')
    inputGrammer = input().split('->')

print('\nGrammer: ',grammer,'\n')

nonTerminals = list()
terminals = list()
for x in grammer:
    if x[0] not in nonTerminals:
        nonTerminals.append(x[0])
    temp = list(x[1])
    for i in temp:
        if 96 < ord(i)< 123:
            if i not in terminals:
                terminals.append(i)

terminals.append('$')

table = [[0 for x in terminals] for y in nonTerminals]
print('NonTerminals: ',nonTerminals,'\n')
print('Terminals: ',terminals,'\n')

def findFirst(notTerm):
    finded = list()
    for g in grammer:
        if g[0] == notTerm:
            if g[1][0] in terminals:
                finded.extend(g[1][0])
            elif g[1][0] in nonTerminals and g[1][0] != '&':
                finded.extend(findFirst(g[1][0]))
            else:
                finded.extend(findFollow(g[0]))
    return finded

def findFollow(notTerm):
    finded = list()
    for g in grammer:
        temp = list(g[1])
        if notTerm in temp and temp[-1] == notTerm:
            finded.extend('$')
        elif notTerm in temp:
            nextNotTerm = temp[temp.index(notTerm)+1]
            if nextNotTerm in terminals:
                finded.extend(nextNotTerm)
            elif nextNotTerm in nonTerminals:
                findedFirst = findFirst(nextNotTerm)
                finded.extend(findedFirst)
    return finded

error = 0
for gr in grammer:
    if error:
        break
    if gr[1][0] in terminals:
        if table[nonTerminals.index(gr[0])][terminals.index(gr[1][0])] != 0:
            break
        else:
            table[nonTerminals.index(gr[0])][terminals.index(gr[1][0])] = gr[2]
    elif gr[1][0] in nonTerminals and gr[1][0] != '&':
        findedFirst = findFirst(gr[1][0])
        for f in findedFirst:
            if table[nonTerminals.index(gr[0])][terminals.index(f)] !=0:
                print('Grammer is not LL1')
                error = 1
                break
            else:
                table[nonTerminals.index(gr[0])][terminals.index(f)] = gr[2]
    elif gr[1][0] == '&':
        findedFollow = findFollow(gr[0])
        for f in findedFollow:
            if table[nonTerminals.index(gr[0])][terminals.index(f)] !=0:
                print('Grammer is not LL1')
                error = 1
                break
            else:
                table[nonTerminals.index(gr[0])][terminals.index(f)] = gr[2]

print('Grammer is LL1')
