import re


def main():
    ignore = {"PUNCT", "NUM", "PART", "SYM"}
    skip = re.compile(r'[,@"()+_[:#*%$<>]|www', re.UNICODE)
    output = {}
    # Data taken from https://tmh.conlang.org/word-frequency/#full-list
    with open("amalgum-frequency-list.csv", encoding="utf-8") as f:
        for i, line in enumerate(f):
            _, count, word, word_type, _, _ = line.split("\t")
            if word_type in ignore or skip.search(word):
                continue
            output[word] = output.get(word, 0) + int(count)


    with open("word_output.txt", "w", encoding="utf-8") as out:
        for word in sorted(output):
            out.write(f"{word},{output[word]}\n")

if __name__ == "__main__":
    main()
