# Unicode Trie with extensions

The normal Trie data structure allows you to access data with keys that consist of lower case ASCII
characters only. This is an extended version that works with Unicode characters, although it is
designed with European languages in mind as it includes support for accented characters where you
can access them by using the unaccented version. It also includes full search on the keyspace for
words in a given edit distance.

It supports most of the features of the built in dictionary, but also includes an enumerator for
words from a given prefix. A wildcard search feature, so h?ll? would find hello for example, this
would be useful in a Wordle type game, scrabble or crossword program. It also has a search for words
with the given edit distance, and has a dictionary of over 100,000 English language words.


    For example searching for fiance will return the following words and edit distances. The edit distance
    takes into account accent addition, transposition, insertion, deletion, case difference, modification.
    Search: fiance
    Distance:
    1 fiancee
    1 fiancé
    1 finance
    2 Defiance
    2 Finance
    2 affiance
    2 defiance
    2 face
    2 fiacre
    2 fine
    3 Diane
    3 Face
    3 Fane
    3 Fian
    3 Fine
    3 France
    3 Wiane
    3 ace
    3 acne
    3 anche
    3 ane
    3 dance
    3 facie
    3 faece
    3 faic
    3 fain
    3 fan
    3 fancy
    3 farce
    3 fence
    3 fiant
    3 fie
    3 fin
    3 finale
    3 finch
    3 finke
    3 finse
    3 fkine
    3 flanc
    3 franc
    3 ian
    3 ice
    3 inc
    3 ine
    3 lance
    3 mince
    3 nance
    3 ofice
    3 pince
    3 since
    3 vince
    3 wince
