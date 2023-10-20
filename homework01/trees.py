#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version 0.1

Cílem je vykreslit v "UTF16-artu" strom definovaný listem hodnot.
Každý vnitřní uzel stromu obsahuje vždy dvě položky: název uzlu a seznam potomků
 (nemusí být nutně v tomto pořadí). Názvem může být jakýkoli objekt kromě typu list (seznam).

Příklady validních stromů:
    - triviální strom o 1 uzlu: [1, []]
    - triviální strom o 1 uzlu s opačným pořadím ID a potomků: [[], 2]
    - triviální strom o 3 uzlech: [1, [2, 3]]
        (listové uzly ve stromu o výšce >= 2 mohou být pro zjednodušení zapsány i bez prázdného seznamu potomků)

Příklady nevalidních stromů:
    - None
    - []
    - [666]
    - [1, 2]
    - (1, [2, 3])


Strom bude vykreslen podle následujících pravidel:
    - Vykresluje se shora dolů, zleva doprava.
    - Uzel je reprezentován jménem, které je stringovou serializací objektu daného v definici uzlu.
    - Uzel v hloubce N bude odsazen zlava o N×{indent} znaků, přičemž hodnota {indent} bude vždy kladné celé číslo > 1.
    - Má-li uzel K potomků, povede:
        - k 1. až K-1. uzlu šipka začínající znakem ├ (UTF16: 0x251C)
        - ke K. uzlu šipka začínající znakem └ (UTF16: 0x2514)
    - Šipka k potomku uzlu je vždy zakončena znakem > (UTF16: 0x003E; klasické "větší než").
    - Celková délka šipky (včetně úvodního znaku a koncového ">") je vždy {indent}, výplňovým znakem je zopakovaný znak ─ (UTF16: 0x2500).
    - Všichni potomci uzlu jsou spojeni na úrovni počátku šipek svislou čarou │ (UTF16: 0x2502); tedy tam, kde není jako úvodní znak ├ nebo └.
    - Pokud název uzlu obsahuje znak `\n` neodsazujte nijak zbytek názvu po tomto znaku.
    - Každý řádek je ukončen znakem `\n`.

Další požadavky na vypracovní:
    - Pro nevalidní vstup musí implementace vyhodit výjimku `raise Exception('Invalid tree')`.
    - Mít codestyle v souladu s PEP8 (můžete ignorovat požadavek na délku řádků - C0301 a používat v odůvodněných případech i jednopísmenné proměnné - C0103)
        - otestujte si pomocí `pylint --disable=C0301,C0103 trees.py`
    - Vystačit si s buildins metodami, tj. žádné importy dalších modulů.


Příklady vstupu a výstupu:
INPUT:
[[[1, [True, ['abc', 'def']]], [2, [3.14159, 6.023e23]]], 42]

PARAMS:
    indent = 4
    separator = '.'

OUTPUT:
42
├──>1
│...└──>True
│.......├──>abc
│.......└──>def
└──>2
....├──>3.14159
....└──>6.023e+23

INPUT:
[[[1, [[True, ['abc', 'def']], [False, [1, 2]]]], [2, [3.14159, 6.023e23, 2.718281828]], [3, ['x', 'y']], [4, []]], 42]

PARAMS:
    indent = 4
    separator = '.'

OUTPUT:
42
├──>1
│...├──>True
│...│...├──>abc
│...│...└──>def
│...└──>False
│.......├──>1
│.......└──>2
├──>2
│...├──>3.14159
│...├──>6.023e+23
│...└──>2.718281828
├──>3
│...├──>x
│...└──>y
└──>4

INPUT:
[6, [[[[1, [2, 3]], [42, [-43, 44]]], 4], 5]]

PARAMS:
    indent = 2
    separator = ' '

OUTPUT:
6
└>5
  └>4
    ├>1
    │ ├>2
    │ └>3
    └>42
      ├>-43
      └>44

INPUT:
[6, [5, ['dva\nradky']]]

PARAMS:
    indent = 2
    separator = ' '

OUTPUT:
6
└>5
  └>dva
radky

Potřebné UTF16-art znaky:
└ ├ ─ │

Odkazy:
https://en.wikipedia.org/wiki/Box_Drawing
"""


class InvalidTree(Exception):
    """Tree is invalid"""


def printFinal( tree: list = None, indent: int = 2, parent: str =' ' ) -> str:
    """Prints lists of tree"""
    string = ''
    for i in enumerate(tree):
        if i[0] != len(tree) - 1:
            string = string + parent + '├' + (indent-2)*'─' + '>' + str(tree[i[0]]) + '\n'
        else:
            string = string + parent + '└' + (indent-2)*'─' + '>' + str(tree[i[0]]) + '\n'
    return string


def printNode ( tree: list = None, indent: int = 2, isLast: bool = True, parent: str = '' ) -> str:
    """Prints a node of tree that is not a list"""
    if isLast:
        string = parent + '└' + (indent-2)*'─' + '>' + str(tree[0]) + '\n'
    else:
        string = parent + '├' + (indent-2)*'─' + '>' + str(tree[0]) + '\n'
    return string


def makeCorrect(tree: list = None):
    """Swaps elements in list so root will always be on 0th index"""
    if isinstance(tree[0], list):
        tree[0], tree[1] = tree[1], tree[0]


def printRoot(tree: list = None, indent: int = 2, parent: str = '', isLast: bool = True, root: bool = False) -> str:
    """Prints root of a current list"""
    makeCorrect(tree)
    if root:
        string = str(tree[0]) + '\n'
    else:
        string = printNode(tree, indent, isLast, parent)
    return string


def render_rec(tree: list = None, indent: int = 2, separator: str = ' ', prefix: list = None, pair: list = None ) -> str:
    """Recursively prints tree"""
    isList = False
    for i in tree:
        if isinstance(i, list):
            isList = True
    if (not isList and pair[1]) or (tree is None) or (not isinstance(tree, list)):
        raise InvalidTree('Invalid tree')
    if isList is False:
        return printFinal( tree, indent, prefix[0] )
    string = printRoot(tree, indent, prefix[0], pair[0], pair[1])
    listOfLists = True
    for i in tree[1]:
        if not isinstance(i, list):
            listOfLists = False
    if listOfLists:
        for i in range (0,len(tree[1])):
            if i != len(tree[1]) - 1:
                string = string + render_rec( tree[1][i], indent, separator, [prefix[1], prefix[1] + '│' + separator * (indent - 1)], [False, False] )
            else:
                string = string + render_rec( tree[1][i], indent, separator, [prefix[1], prefix[1] + separator * (indent)], [True, False] )
    else:
        string = string + render_rec( tree[1], indent, separator, [prefix[1], prefix[1] + separator * (indent)], [True, False] )
    return string


def render_tree(tree: list = None, indent: int = 2, separator: str = ' ') -> str:
    """Calls recursive function"""
    return render_rec ( tree, indent, separator, ['', ''], [True, True])


print(render_tree([[[1, [True, ['abc', 'def']]], [2, [3.14159, 6.023e23]]], 42], 4, '.'))
print(render_tree([6, [[[[1, [2, 3]], [42, [-43, 44]]], 4], 5]], 2, ' '))
print(render_tree([[[1, [[True, ['abc', 'def']], [False, [1, 2]]]], [2, [3.14159, 6.023e23, 2.718281828]], [3, ['x', 'y']], [4, []]], 42], 4, '.'))
print(render_tree([6, [5, ['dva\nradky']]], 2, ' '))
print(render_tree([[[1, [2, [4, 5]]], [42, [43, 44]]], 3], 4, ' '))

try:
    print(render_tree([], 4, ' '))
except InvalidTree:
    print("None")
try:
    print(render_tree([666], 4, ' '))
except InvalidTree:
    print("666")
try:
    print(render_tree([1,2], 4, ' '))
except InvalidTree:
    print("1,2")
try:
    print(render_tree((1,[2,3]), 4, ' '))
except InvalidTree:
    print("())")

# l = [1,2,3]
# for i in enumerate(l):
#     print(i)
