from ..utils.score import all_words, calc_score, answers
from ..utils.solve import generate_elim_guesses2, words_with_unused_letters, count_common_words, narrow_common_sort, broad_common_sort
import numpy as np
import pandas as pd

def test_filter_words(guess, color_code, word_dict, narrow_sort_threshold): 
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

    if len(word_dict) < narrow_sort_threshold:
        word_dict = narrow_common_sort(word_dict)
        pass
    #if len(word_dict) < 350:
    word_dict = broad_common_sort(word_dict)

    return word_dict

#tests algorithm on all possible wordle answers with customizable features of the algorithm
#param: positional_weight = the weight given to each letter of a word based on its frequency in that position
#param: overall_weight = the weight given to each letter of a word based on its overall frequency
#return: avg_guesses = the average number of guesses it took the algorithm to solve a given wordle, excluding wordles that take over 6 guesses
#return: unsolved = dictionary with keys of words that took over 6 guesses and values of the number of guesses that word took
def test_algorithm(positional_weight, overall_weight):
    scored_words = {}
    for word in all_words:
        scored_words[word] = calc_score(word, positional_weight, overall_weight)

    scored_words = dict(sorted(scored_words.items(), key=lambda item: item[1], reverse=True))
    total_guesses = 0
    unsolved = {}
    for i, word in enumerate(answers):
        #print(f"{round(100 * i/len(answers))}%: {word}")
        num_guesses = run_wordle(word, scored_words, narrow_sort_threshold=36)
        if num_guesses > 6:
            unsolved[word] = num_guesses
            total_guesses += num_guesses
        else:
            total_guesses += num_guesses
        


    avg_num_guesses = total_guesses / (len(answers))

    print_stats(avg_num_guesses, positional_weight, overall_weight, unsolved)

    return avg_num_guesses, unsolved

#prints the stats of the algorithm after going through all possible wordle answers
def print_stats(avg_guesses, positional_weight, overall_weight, unsolved_words):
    print()
    print("Algorithm: ")
    print(f"Weight of positional letter frequencies: {positional_weight}")
    print(f"Weight of overall letter frequencies: {overall_weight}")
    print()
    print(f"It took the algorithm an average of {round(avg_guesses, 4)} guesses to solve a given wordle, excluding unsolved wordles")
    print(f"There were {len(unsolved_words)} out of {len(answers)} unsolved wordles (over 6 guesses)")
    percent_unsolved = round((100 * len(unsolved_words) / len(answers)), 2)
    print()
    print(f"Your algorithm was able to solve {100 - percent_unsolved}% of wordles")
    print(f"Your algorithm was unable to solve {percent_unsolved}% of wordles")

#auto solves a wordle with a given answer and returns the number of guesses it took the algorithm 
#param: answer, the answer to the wordle
#param: scored_words, a dictionary of five letter words scored and sorted based on positional and overall letter frequency
def run_wordle(answer, scored_words, narrow_sort_threshold):
    num_guesses = 0
    color_code = 'xxxxx'
    word_dict = scored_words.copy()
    used_letters = []
    correct_letters = []
    elim_dict = {}

    current_guess = list(word_dict)[0]

    while(color_code != 'ggggg'):
        #print(current_guess)
        color_code = compare_answer(current_guess, answer)

        num_guesses += 1

        word_dict = test_filter_words(current_guess, color_code, word_dict, narrow_sort_threshold)

        for i, char in enumerate(color_code):
                if char != 'x' and current_guess[i] not in correct_letters:
                    correct_letters.append(current_guess[i])
            
        if num_guesses < 2: 
            common_words_left = count_common_words(list(word_dict))
            if len(common_words_left) < 3:
                current_guess = list(word_dict)[0]
            elif len(word_dict) < 45:
                current_guess = (generate_elim_guesses2(common_words_left, color_code, correct_letters))[0]
            else:
                for char in current_guess:
                    if char not in used_letters:
                        used_letters.append(char)
                elim_dict = words_with_unused_letters(used_letters)
                current_guess = list(elim_dict)[0]
        elif color_code.count('g') >= 3 and num_guesses < 5:
            common_words_left = count_common_words(list(word_dict))
            if len(common_words_left) > 3:
                current_guess = (generate_elim_guesses2(common_words_left, color_code, correct_letters))[0]
            else:
                current_guess = list(word_dict)[0]
        else:
            current_guess = list(word_dict)[0]
        
    return num_guesses

#compares a guess to an answer and returns the corresponding color code
def compare_answer(guess, answer):
    color_code = [None] * 5
    temp_answer = list(answer)
    already_assigned = []
    for i, char in enumerate(guess):
        if char == temp_answer[i]:
            color_code[i] = 'g'
            temp_answer[i] = '_'
            already_assigned.append(i)
    for i, char in enumerate(guess):
        if char in temp_answer and char != temp_answer[i] and i not in already_assigned:
            color_code[i] = 'y'
            temp_answer[temp_answer.index(char)] = '_'
    for i, char in enumerate(guess):
        if color_code[i] == None:
            color_code[i] = 'x'

    return ''.join(color_code)

#finds average guesses of different scoring weights with a set elimination threshold
def optimize_weights():
    scoring_weight_evaluation = [] #to be list of dictionaries that will be converted to data frame

    for number in np.arange(0, 2.1, 0.05):
        current_row = {}
        positional_weight = round(number, 1)
        overall_weight = 1
        avg_guesses,_ = test_algorithm(positional_weight, overall_weight)

        current_row['overall_weight'] = overall_weight
        current_row['positional_weight'] = positional_weight
        current_row['avg_guesses'] = avg_guesses

        scoring_weight_evaluation.append(current_row)
        
    df = pd.DataFrame(scoring_weight_evaluation)
    return df

def main():
    
    #Test cases for compare_answer()
    #print(compare_answer('mired', 'wider'))
    #print(compare_answer('linty', 'bagel'))
    #print(compare_answer('paled', 'bagel'))
    #print(compare_answer('elect', 'elect'))

    pd.set_option('display.max_rows', None)

    #df = optimize_weights(elim_threshold=350)

    '''min_index = df['avg_guesses'].idxmin()
    min_row = df.loc[min_index]
    print("\nAlgorithm with lowest average guesses:")
    print(min_row)
    print(df)'''


    scored_words = {}
    for word in all_words:
        scored_words[word] = calc_score(word, 0.2, 1)

    scored_words = dict(sorted(scored_words.items(), key=lambda item: item[1], reverse=True))

    #run_wordle('piano', scored_words)

    unsolved_words = {}

    avg_guesses, unsolved_words = test_algorithm(0.5, 1, )

    for word, num_guesses in unsolved_words.items():
        #print(f"{word}: {num_guesses}")
        pass


if __name__ == "__main__":
    main()