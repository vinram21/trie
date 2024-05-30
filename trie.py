import itertools

class Trie:
    """
    A Trie is a data structure similar to a dictionary, that is sorted
    and can also allow searches for prefixes
    """

    def __init__(self) -> None:

        """
        Create an instance of a trie

        >>> trie = Trie()
        >>> len(trie)
        0
        >>> trie["test"] = "OK"
        >>> "test" in trie
        True
        >>> "missing" in trie
        False
        """
        self.words = {}
        self.size = 0

    def _entry(self, word : str) -> {}:

        """
        Search the trie and find the dictionary for the end of word
        :param word: Word to find in the tree (or prefix)
        :return: dictionary of the end of the word

        >>> trie = Trie()
        >>> trie += "hello"
        >>> trie += "world"
        >>> trie._entry("worl")
        {'d': {'.': True}}
        """
        curr = self.words
        for letter in word:
            if letter in curr:
                curr = curr[letter]
            else:
                return {}
        return curr

    def _insert(self, word : str, value : any = True) -> {}:

        """
        Insert a new value into the Trie (or overwrite an existing one)
        :param word: The key to insert
        :param value: The value to store
        :return: The dictionary entry at the end of the word
        >>> trie = Trie()
        >>> trie._insert("hello", "world")
        {'.': 'world'}
        """
        if word.isalpha() and word.islower():
            curr = self.words
            for letter in word:
                if letter in curr:
                    curr = curr[letter]
                else:
                    curr[letter] = {}
                    curr = curr[letter]
            if '.' not in curr:
                self.size += 1
            curr['.'] = value  # To mark full word
            return curr
        else:
            raise KeyError("Only lower case words accepted")

    def __iadd__(self, word : str) -> "self":

        """
        Add new entry to Trie

        :param word: Word to add
        :return: The updated Trie
        >>> trie = Trie()
        >>> trie += "test"
        >>> "test" in trie
        True
        """
        curr = self._insert(word)
        return self

    def __isub__(self, word : str) -> "self":

        """
        Remove entry in Trie

        :param word: Word to remove
        :return: The updated Trie
        >>> trie = Trie()
        >>> trie += "test"
        >>> "test" in trie
        True
        >>> trie -= "test"
        >>> "test" in trie
        False
        """
        curr = self._entry(word)
        if '.' in curr:
            self.size -= 1
            del curr['.']
        return self


    def __contains__(self, word : str) -> bool:

        """
        Check if value is in trie

        :param word: Word to check
        :return: True if word is in trie
        >>> trie = Trie()
        >>> trie += "hello"
        >>> "hello" in trie
        True
        >>> "hell" in trie  # Prefix should not be recognized as a word
        False
        """
        curr = self._entry(word)
        return '.' in curr

    def __getitem__(self, word : str) -> any:

        """
        Provide dictionary style access to trie

        :param word: Key to get
        :return: Value in trie (or KeyError if not found)
        >>> trie = Trie()
        >>> trie += "hello"
        >>> trie["hello"]
        True
        >>> trie["hell"]  # Prefix should not be recognized as a word
        Traceback (most recent call last):
        ...
        KeyError: '.'
        """
        curr = self._entry(word)
        return curr['.']

    def __setitem__(self, key : str, value : any) -> None:

        """
        Set value in Trie

        :param key: The word to insert
        :param value: The value return when querying it
        :return: Value in trie
        >>> trie = Trie()
        >>> trie["hello"] = "world"
        >>> trie["hello"]
        'world'
        """
        curr = self._insert(key, value)

    def get(self, word : str, default : any = None) -> any:

        """
        Get value or default if the key does not exist

        :param word: The key to search
        :param default: Value to return if the key is not in the trie
        :return: value in trie or default if value is not present
        >>> trie = Trie()
        >>> trie.get("hello", "missing")
        'missing'
        >>> trie["hello"] = "world"
        >>> trie.get("hello")
        'world'
        """
        curr = self._entry(word)
        return curr.get('.', default)


    def __delitem__(self, word : str) -> None:

        """
        Delete item from trie

        :param word: Word to delete
        :return: None
        >>> trie = Trie()
        >>> trie["hello"] = "world"
        >>> trie.get("hello")
        'world'
        >>> del trie["hello"]
        >>> del trie["hello"]
        Traceback (most recent call last):
        ...
        KeyError: '.'
        """
        curr = self._entry(word)
        del curr['.']
        self.size -= 1

    def load(self, filename : str) -> None:

        """
        Load the contents of a file of words to the trie

        :param filename: File to load
        :return: None

        >>> trie = Trie()
        >>> trie.load("words850.txt")
        >>> trie
        <trie 850 words ['a', 'able', 'about', '...']>
        """
        with open(filename) as f:
            for line in f:
                self += line.strip()


    def __str__(self):

        """
        Return a string representation of the trie

        :return: Number of words, and first 3 words

        >>> trie = Trie()
        >>> trie += "hello"
        >>> trie += "world"
        >>> trie
        <trie 2 words ['hello', 'world']>
        >>> trie += "test"
        >>> trie += "testing"
        >>> trie
        <trie 4 words ['hello', 'test', 'testing', '...']>
        """
        return repr(self)

    def __len__(self):

        """
        Return the number of words in the trie

        :return: The number of words in the trie
        >>> trie = Trie()
        >>> trie += "hello"
        >>> trie += "world"
        >>> len(trie)
        2
        >>> trie += "test"
        >>> trie += "test"
        >>> len(trie)
        3
        """
        return self.size

    def _keys(self, prefix : str, curr : {}) -> (...):

        """
        List all the keys in the tree starting at a given prefix
        :param prefix: The start of the word
        :param curr: The current dictionary
        :return: Generator with items sorted in alphabetical order

        >>> trie = Trie()
        >>> trie += "hello"
        >>> trie += "world"
        >>> list(trie._keys("", trie.words))
        ['hello', 'world']
        """
        if "." in curr:
            yield prefix
        for ch in sorted(curr):
            if ch != '.':
                yield from self._keys(prefix + ch, curr[ch])

    def __iter__(self):

        """
        Iterator with all of the words in the trie
        :return: Iterator
        >>> trie = Trie()
        >>> trie += "hello"
        >>> trie += "world"
        >>> [word for word in trie]
        ['hello', 'world']
        """
        yield from self._keys("", self.words)

    def prefix(self, word : str):

        """
        List all the words starting with prefix (for autocomplete)

        :param word: The start of words
        :return: Generator with all the words starting with a prefix

        >>> trie = Trie()
        >>> trie += "hello"
        >>> trie += "world"
        >>> trie += "help"
        >>> [word for word in trie.prefix("hel")]
        ['hello', 'help']
        """
        curr = self._entry(word)
        yield from self._keys(word, curr)

    def __repr__(self):

        """
        Return a string representation of the trie
        :return: Number of words, and first 3 words

        >>> trie = Trie()
        >>> trie += "hello"
        >>> trie += "world"
        >>> trie
        <trie 2 words ['hello', 'world']>
        """
        words = [word for word in itertools.islice(self, 3)]
        if len(self) > 3:
            words.append("...")
        return f"<trie {self.size} words {words}>"


    def _search(self, prefix : str, key : str, curr : {}) -> (...):

        if not key:
            if "." in curr:
                yield prefix
        else:
            if key[0] == '?':
                for ch in sorted(curr):
                    if ch != '.':
                        yield from self._search(prefix + ch, key[1:], curr[ch])
            elif key[0] in curr:
                yield from self._search(prefix + key[0], key[1:], curr[key[0]])

    def search(self, key : str) -> [str,...]:

        """
        Search the trie for any matching words a ? means a wildcard that matches anything

        :param word: The partial word to search for (? indicates any character, so f?n matches fan, fin, fun)
        :return: Generator returning words that match the wildcard specification
        >>> trie = Trie()
        >>> trie += "hello"
        >>> trie += "world"
        >>> [word for word in trie.search("h??l?")]
        ['hello']
        >>> [word for word in trie.search("???l?")]
        ['hello', 'world']
        """

        yield from self._search("", key, self.words)

    def _spellcheck(self, prefix : str, key : str, diff : int, curr : {}):
        if diff > 3:
            return
        if not key:
            if "." in curr:
                yield diff, prefix
        else:
            expect = key[0]
            if len(key) > 1:
                nextCh = key[1]
                if nextCh in curr and expect in curr[nextCh]:
                    # Transpose the characters
                    yield from self._spellcheck(prefix + nextCh + expect, key[2:], diff + 1, curr[nextCh][expect])
                # Delete character
                yield from self._spellcheck(prefix, key[1:], diff + 1, curr)
            else:
                yield from self._spellcheck(prefix, key[1:], diff + 1, curr)
            for ch in sorted(curr):
                if ch != '.':
                    # Insert a character
                    yield from self._spellcheck(prefix + ch, key, diff + 1, curr[ch])
                    if ch != expect:
                        # Different letter (difference 1)
                        yield from self._spellcheck(prefix + ch, key[1:], diff + 1, curr[ch])
                    else:
                        # Expected letter (difference 0)
                        yield from self._spellcheck(prefix + ch, key[1:], diff, curr[ch])

    def spellcheck(self, word : str):

        """
        Return a list of words based on their Levenshtein distance (+1 for each letter change,
        insertion, deletion, transposition)

        :param word: The word to check
        :return: List with tuples of distance and alternate spellings
        >>> trie = Trie()
        >>> trie += "hello"
        >>> trie += "help"
        >>> trie += "hell"
        >>> trie += "shell"
        >>> trie += "shall"
        >>> trie.spellcheck("hello")
        [(0, 'hello'), (1, 'hell'), (2, 'help'), (2, 'shell'), (3, 'shall')]
        """
        maybe = {}
        for (diff, word) in self._spellcheck("", word, 0, self.words):
            maybe[word] = min(maybe.get(word, 100), diff)
        possible = [(item[1], item[0]) for item in maybe.items()]
        possible.sort()
        return possible


def main():
    trie = Trie()
    trie.load("words850.txt")
    print("humour" in trie)
    print(trie)
    trie["humour"] = "humor"
    print("humour" in trie)
    print(trie.get("humour", False))
    #del trie["humour"]
    trie -= "humour"
    print("humour" in trie)
    print(len(trie))
    for word in trie.prefix("fi"):
        print(word)
    print("Search:")
    for word in trie.search("f?r?"):
        print(word)
    print("Spellcheck:")
    for diff, word in trie.spellcheck("fork"):
        print(diff, word)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()