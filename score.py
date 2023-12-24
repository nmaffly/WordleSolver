import json
from stats import read_file

positional_frequencies_file = 'positional_frequencies.json'
overall_frequencies_file = 'overall_frequencies.json'

# load frequencies from a JSON file
def load_frequencies_from_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)
    
#calculates the score for a word based on each letter frequency
def calc_score(word):
    global pos_frequencies
    global overall_frequencies

    score = 0

    seen_letters = set()

    for index, letter in enumerate(word):
        if letter in seen_letters:
            continue

        seen_letters.add(letter)

        if letter in positional_frequencies[index]:
            score += positional_frequencies[index][letter] #* 5
        
        score += overall_frequencies[letter]    
    
    return score

positional_frequencies = load_frequencies_from_file(positional_frequencies_file)
overall_frequencies = load_frequencies_from_file(overall_frequencies_file)

all_words = read_file('words/allowed_words.txt')

scored_words = {}

for word in all_words:
    scored_words[word] = calc_score(word)
    
scored_words = dict(sorted(scored_words.items(), key=lambda item: item[1], reverse=True))


def main():

    test_word = 'hello'
    score = calc_score(test_word)
    print(f"The score for {test_word} is {score}")
    
    i = 0
    for word, word_score in scored_words.items():
        print(f"{word}: {word_score}")
        i += 1
        if (i == 15):
            break

if __name__ == "__main__":
    main()