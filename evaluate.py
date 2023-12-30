from score import common_words, all_words, calc_score, answers
from solve import filter_words, generate_elim_guesses2, words_with_unused_letters, count_common_words
import numpy as np
import pandas as pd

#tests algorithm on all possible wordle answers with customizable features of the algorithm
#param: positional_weight = the weight given to each letter of a word based on its frequency in that position
#param: overall_weight = the weight given to each letter of a word based on its overall frequency
#param: elim_threshold = the number of possible words left before the elimination guesses are no longer used
#return: avg_guesses = the average number of guesses it took the algorithm to solve a given wordle, excluding wordles that take over 6 guesses
#return: unsolved = dictionary with keys of words that took over 6 guesses and values of the number of guesses that word took
def test_algorithm(positional_weight, overall_weight, elim_threshold):
    scored_words = {}
    for word in all_words:
        scored_words[word] = calc_score(word, positional_weight, overall_weight)

    scored_words = dict(sorted(scored_words.items(), key=lambda item: item[1], reverse=True))
    total_guesses = 0
    unsolved = {}
    for i, word in enumerate(answers):
        #print(f"{round(100 * i/len(answers))}%: {word}")
        num_guesses = run_wordle(word, scored_words, elim_threshold)
        if num_guesses > 6:
            unsolved[word] = num_guesses
            total_guesses += num_guesses
        else:
            total_guesses += num_guesses
        


    avg_num_guesses = total_guesses / (len(answers))

    print_stats(avg_num_guesses, positional_weight, overall_weight, unsolved, elim_threshold)

    return avg_num_guesses, unsolved

#prints the stats of the algorithm after going through all possible wordle answers
def print_stats(avg_guesses, positional_weight, overall_weight, unsolved_words, elim_threshold):
    print()
    print("Algorithm: ")
    print(f"Weight of positional letter frequencies: {positional_weight}")
    print(f"Weight of overall letter frequencies: {overall_weight}")
    print(f"Elimination guess threshold: {elim_threshold}")
    print()
    print(f"It took the algorithm an average of {round(avg_guesses, 4)} guesses to solve a given wordle, excluding unsolved wordles")
    print(f"There were {len(unsolved_words)} out of {len(answers)} unsolved wordles (over 6 guesses)")
    percent_unsolved = round((100 * len(unsolved_words) / len(answers)), 2)
    print()
    print(f"Your algorithm was able to solve {100 - percent_unsolved}% of wordles")
    print(f"Your algorithm was unable to solve {percent_unsolved}% of wordles")

#auto solves a wordle with a given answewr and returns the number of guesses it took the algorithm 
#param: answer, the answer to the wordle
#param: scored_words, a dictionary of five letter words scored and sorted based on positional and overall letter frequency
#param: elim_threshold, the number of possible words left before the elimination guesses are no longer used
def run_wordle(answer, scored_words, elim_threshold):
    num_guesses = 0
    color_code = 'xxxxx'
    word_dict = scored_words.copy()
    used_letters = []
    correct_letters = []
    elim_dict = {}

    current_guess = list(word_dict)[0]

    while(color_code != 'ggggg'):
        color_code = compare_answer(current_guess, answer)

        num_guesses += 1

        word_dict = filter_words(current_guess, color_code, word_dict)

        for i, char in enumerate(color_code):
                if char != 'x' and current_guess[i] not in correct_letters:
                    correct_letters.append(current_guess[i])

        if num_guesses < 2 or len(word_dict) > elim_threshold: 
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

#finds average guesses of different elimination thresholds with set scoring weights
def optimize_elim_threshold(positional_weight, overall_weight):
    elim_threshold_evaluation = []

    print("Elimination threshold: avg number of guesses to solve")
    for elim_threshold in range(325, 376):
        avg_guesses, _ = test_algorithm(positional_weight, overall_weight, elim_threshold)
        elim_threshold_evaluation[elim_threshold] = avg_guesses
        print(f"{elim_threshold}: {avg_guesses}")
    
    most_efficient = min(elim_threshold_evaluation, key=lambda k: elim_threshold_evaluation[k])
    print()
    print(f"The most efficient elimination threshold was {most_efficient} with an average number of guesses of {elim_threshold_evaluation[most_efficient]}")

#finds average guesses of different scoring weights with a set elimination threshold
def optimize_weights(elim_threshold):
    scoring_weight_evaluation = [] #to be list of dictionaries that will be converted to data frame

    for number in np.arange(0, 2.1, 0.1):
        current_row = {}
        positional_weight = round(number, 1)
        overall_weight = 1
        avg_guesses,_ = test_algorithm(positional_weight, overall_weight, elim_threshold)

        current_row['overall_weight'] = overall_weight
        current_row['positional_weight'] = positional_weight
        current_row['avg_guesses'] = avg_guesses

        scoring_weight_evaluation.append(current_row)
        
    df = pd.DataFrame(scoring_weight_evaluation)
    return df

def evaluate_algorithm():
    evaluation = [] #dictionary where key value pair is positional weight and corresponding avg guesses
    for elim_threshold in [100, 150, 200, 250, 300, 350, 400]:  
        for number in np.arange(0, 2.1, 0.1):
            current_row = {}
            positional_weight = round(number, 1)
            overall_weight = 1
            avg_guesses,_ = test_algorithm(positional_weight, overall_weight, elim_threshold)

            current_row['elim_threshold'] = elim_threshold
            current_row['overall_weight'] = overall_weight
            current_row['positional_weight'] = positional_weight
            current_row['avg_guesses'] = avg_guesses
            print("|", end="", flush=True)
            evaluation.append(current_row)
        
    df = pd.DataFrame(evaluation)
    return df   

def main():
    
    #Test cases for compare_answer()
    print(compare_answer('mired', 'wider'))
    #print(compare_answer('linty', 'bagel'))
    #print(compare_answer('paled', 'bagel'))
    #print(compare_answer('elect', 'elect'))
    

    '''
    evaluation_df = evaluate_algorithm()

    pd.set_option('display.max_rows', None)
    print(evaluation_df)

    max_index = evaluation_df['avg_guesses'].idxmax()
    max_row = evaluation_df.loc[max_index]
    print("\nAlgorithm with highest average guesses:")
    print(max_row)
    evaluation_df.to_csv('algorithms.csv', index=False)
    '''


    scored_words = {}
    for word in all_words:
        scored_words[word] = calc_score(word, 0.2, 1)

    scored_words = dict(sorted(scored_words.items(), key=lambda item: item[1], reverse=True))

    #run_wordle('baker', scored_words, elim_threshold=350)

    unsolved_words = {}

    #avg_guesses, unsolved_words = test_algorithm(0.2, 1, 350)

    for word, num_guesses in unsolved_words.items():
        #print(f"{word}: {num_guesses}")
        pass


if __name__ == "__main__":
    main()