import json

# count frequencies of letters in each position
def count_letter_frequencies(word_list):
    pos_frequencies = [{} for _ in range(5)] #array of dictionary containing positional frequencies
    overall_frequencies = {} #dictionary of letter frequencies
    total_words = 0

    for word in word_list:
        if word[4] != 's':
            total_words += 1
            for index, letter in enumerate(word):
                #counting positional frequencies
                if letter not in pos_frequencies[index]:
                    pos_frequencies[index][letter] = 1
                else:
                    pos_frequencies[index][letter] += 1
                
                #counting overall letter frequencies
                if letter not in overall_frequencies:
                    overall_frequencies[letter] = 1
                else:
                    overall_frequencies[letter] += 1

    # sort positional frequencies by most to least frequent letters per position
    # Also normalizes each frequency into a percentage (frequency of letter divided by the total number of words)
    for position, letter_dict in enumerate(pos_frequencies):
        sorted_letters = dict(sorted(letter_dict.items(), key=lambda item: item[1], reverse=True))
        total_frequency = sum(sorted_letters.values())  

        normalized_letters = {}  # Create a new dictionary for normalized frequencies
        for letter, frequency in sorted_letters.items():
            normalized_letters[letter] = frequency / total_frequency
        pos_frequencies[position] = normalized_letters
        
    # sorting and normalizing overall frequencies
    overall_frequencies = dict(sorted(overall_frequencies.items(), key=lambda item: item[1], reverse=True))
    for letter, frequency in overall_frequencies.items():
        overall_frequencies[letter] = frequency / (total_words * 5)

    return pos_frequencies, overall_frequencies


# reads file into list
def read_file(file_path):
    with open(file_path, 'r') as file:
        words = [word.strip() for word in file.readlines()]

    return [word for word in words if word.isalpha()]

# save frequencies to a JSON file
def save_frequencies_to_file(frequencies, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(frequencies, json_file, indent=2)


def main():
    path1 = 'words/allowed_words.txt'
    path2 = 'words/common_five_letter_words.txt'
    positional_frequencies_file = 'positional_frequencies.json'
    overall_frequencies_file = 'overall_frequencies.json'

    all_words = read_file(path1)
    positional_frequencies, overall_frequencies = count_letter_frequencies(all_words)
    save_frequencies_to_file(positional_frequencies, positional_frequencies_file)
    save_frequencies_to_file(overall_frequencies, overall_frequencies_file)

    # Display the frequencies
    for position, letter in enumerate(positional_frequencies):
        print(f"Position {position}:")
        for letter, frequency in letter.items():
            print(f"{letter}: {frequency}")
    
    print("\nOverall Letter Frequencies")
    for a, f in overall_frequencies.items():
        print(f"{a}: {f}")

if __name__ == "__main__":
    main()
