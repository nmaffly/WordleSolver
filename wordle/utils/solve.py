from .score import scored_words, common_words, all_words, overall_frequencies

#alphabet as a global variable
all_letters = [chr(ord('a') + i) for i in range(26)] 

def filter_words(guess, color_code, word_dict): 
    guess = guess.lower()
    color_code = color_code.lower()
    
    g_pos = []
    y_pos = []
    x_pos = []
    for pos, letter in enumerate(color_code):
        if letter == 'x':
            x_pos.append(pos)
        elif letter == 'y':
            y_pos.append(pos)
        elif letter == 'g':
            g_pos.append(pos)

    words_to_remove = []  # Create a list to store words to be removed

    for word, _ in word_dict.items():
        continue_flag = True
        temp = list(word)

        for pos in g_pos:
            if temp[pos] != guess[pos]:
                words_to_remove.append(word)
                continue_flag = False
                break
            else:
                temp[pos] = '_'
        if continue_flag:
            for pos in y_pos:
                if (temp.count(guess[pos]) < 1) or (temp[pos] == guess[pos]):
                    words_to_remove.append(word)
                    continue_flag = False
                    break
                else:
                    for i, val in enumerate(temp):
                        if val == guess[pos]:
                            temp[i] = '_'
                            break
        if continue_flag:
            for pos in x_pos:
                if guess[pos] in temp:
                    words_to_remove.append(word)
                    break

    # Remove the words outside the loop
    for word in words_to_remove:
        del word_dict[word]

    if len(word_dict) < 36:
        word_dict = narrow_common_sort(word_dict)
        pass
    #if len(word_dict) < 350:
    word_dict = broad_common_sort(word_dict)

    return word_dict

def broad_common_sort(word_dict):
    """
    Sorts the dictionary keys so that keys in common_words are at the front, but maintain their scored order

    :param word_dict: Dictionary of words (keys) and their associated values.
    :param common_words: List of common words to prioritize.
    :return: Sorted dictionary (word, value)
    """ 

    sorted_items = sorted(word_dict.items(), key=lambda item: (item[0] not in common_words, item[0].endswith('s'), item[0].endswith('ed')))

    return dict(sorted_items)

def narrow_common_sort(word_dict):
    """
    Sorts the dictionary keys based on their order in common_words. 
    Words not in common_words are moved to the end.

    :param word_dict: Dictionary of words (keys) and their associated values.
    :return: Sorted dictionary
    """
    # Create a set for faster membership tests
    common_words_set = set(common_words)

    def sort_key(word):
        try:
            # Position in common_words if the word is in common_words
            return common_words.index(word)
        except ValueError:
            # A large number to move the word to the end if it's not in common_words
            return float('inf')

    sorted_items = sorted(word_dict.items(), key=lambda item: (sort_key(item[0]), item[0] not in common_words_set))
    return dict(sorted_items)

def words_with_unused_letters(used_letters):
    copy_dict = scored_words.copy()
    filtered_dict = {}
    letters = used_letters[:]
    
    for word,value in copy_dict.items():
        add = True
        for letter in letters:
            if letter in word:
                add = False
                break
    
        if add:
            filtered_dict[word] = value
        
    return filtered_dict

def count_common_words(word_list):
    remaining_words_set = set(word_list)
    common_words_set = set(common_words)

    remaining_common_words = remaining_words_set.intersection(common_words_set)

    return list(remaining_common_words)

#generates a list of words based on unused letters
def generate_elim_guesses2(word_dict, color_code, correct_letters):
    non_green_indeces = []
    for i, color in enumerate(color_code):
        if color == 'x':
            non_green_indeces.append(i)
    elim_letters =[]

    for word in word_dict:
        for index in non_green_indeces:
            if word[index] not in elim_letters:
                elim_letters.append(word[index])

    letters_set = set(elim_letters) - set(correct_letters)

    word_matches = {}
    for word in all_words:
        count = 0
        used_letters = []
        for letter in word:
            if letter in letters_set and letter not in used_letters:
                count += 1
                used_letters.append(letter)
        word_matches.setdefault(count, []).append(word)

    max_count = max(word_matches.keys())

    words_with_most_matches = word_matches[max_count]


    return words_with_most_matches

#removes any letters from list 'letters' that aren't in any of the words in list 'words'
def remove_letters(letters, words):
    new_letters = []

    for letter in letters:
        remove_letter = True
        for word in words:
            if letter in word:
                new_letters.append(letter)
                break
    
    return new_letters
    
#driver code for solving
def solve():
    word_dict = scored_words.copy()
    elim_dict = {}
    color_code = 'xxxxx'
    guess = ''
    
    unused_letters = all_letters[:]
    used_letters = []
    correct_letters = []

    print("Hi, I'm your virtual wordle assistant!")
    print("Here are some my recommended words to use: ")
    print(list(word_dict.keys())[:10])
    print(f"Possible words left: {len(word_dict)}\n")

    guess = input("Enter your guess: ")
    for char in guess:
            if char not in used_letters:
                used_letters.append(char)
        
    color_code = input("What was the corresponding color code (e.g. xxgyx): ")
    #add correct letters to list
    for i, char in enumerate(color_code):
        if char != 'x' and guess[i] not in correct_letters:
            correct_letters.append(guess[i])
        elif char == 'x' and guess[i] in unused_letters:
            unused_letters.remove(guess[i])
    
    word_dict = filter_words(guess, color_code, word_dict)

    while(color_code != 'ggggg'):
        print(f"Possible words left: {len(word_dict)}")  
        print(f"Used letters: {[letter for letter in all_letters if letter not in used_letters]}")
        
        print("Here are some my elimination words to use: ")
        elim_dict = words_with_unused_letters(used_letters)
        #elim_dict = generate_elim_guesses2(unused_letters, word_dict)
        if elim_dict:
            print(list(elim_dict.keys())[:10])
            print("Here are some possible answers: ")
            print(list(word_dict.keys())[:10])
        else:
            print("There are no possible elimantion words left. Here are possible answers:")
            print(list(word_dict.keys())[:10])

        guess = input("Enter your guess: ")
        #add each letter from your guess to list of used letters
        for char in guess:
            if char not in used_letters:
                used_letters.append(char)

        color_code = input("What was the corresponding color code (e.g. xxgyx): ")
        #add correct letters to list
        for i, char in enumerate(color_code):
            if char != 'x' and guess[i] not in correct_letters:
                correct_letters.append(guess[i])
        

        word_dict = filter_words(guess, color_code, word_dict)
    
    print("Congrats on solving the wordle!")

def main():
    solve()
if __name__ == "__main__":
    main()
