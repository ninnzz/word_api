## Reference: https://github.com/atbaker/wikipedia-question-generator
import re
import random

from newspaper import Article
from textblob import TextBlob
from .textteaser import TextTeaser

def extract_questions(_summarized, _title):
    """ Extracts the questions from an
        article/set of sentences input
    """
    quiz = []
    summ = ' '.join(_summarized)
    # print(summ)
    # summ = re.sub(r'\[[^)]*\]', '', summ)
    summarized = TextBlob(summ)

    ss = summarized.sentences
    np = summarized.noun_phrases
    random.shuffle(np)

    for sentence in ss[1:]:
        qq = analyze_sentence(sentence, _title)
        if qq:
            np = np[4:]
            ch = assign_choices(qq['answer'], np)
            qq['correct_choice'] = ch[0]
            qq['choices'] = ch[1]
            quiz.append(qq)

    return quiz

def assign_choices(words, word_options):
    """ Assign choices
    """
    choices = []

    for wo in word_options:
        if wo != words and wo not in choices:
            choices.append(wo)

        if len(choices) == 4:
            break


    index = round((random.random() * 100) % 3)
    # print(index)
    # print(choices)
    choices[index] = words

    return (index, choices)

def analyze_sentence(sentence, title):
    """ Analyzes the sentence and give out question sentence
    """
    ### Sentences that start with Adverbs are usually supporting sentences
    ### and is not good to use
    tag_filter = ['IN', 'RB']
    if sentence.tags[0][1] in tag_filter or len(sentence.words) < 10:
        return None

    answer = []
    noun_counter = 0
    for word, tag in sentence.tags:
        ### Reminder, add a counter for how many proper nouns to use

        ### Checks if a word is a noun
        ### Nouns are candidate for blanking and adding to question
        if tag == 'NN':

            ### Ignore the first noun
            ### since most articles uses
            ### 'The <noun>' pattern.
            ### The pattern is not a good fit
            if noun_counter == 0:
                noun_counter += 1
                continue

            ### Check if word is a part of a phrase
            for n_phrase in sentence.noun_phrases:
                
                if word in n_phrase:
                    answer += n_phrase.split()[-2:]
                    break
            
            if len(answer) == 0:
                answer.append(word)
        
            break

    ### No words selected
    if not answer:
        return None

    quiz_question = {}
    to_replace = re.compile(re.escape(' '.join(answer)), re.IGNORECASE)
    quiz_question['item'] = to_replace.sub('_____________', str(sentence), count=1)
    quiz_question['answer'] = ' '.join(answer)

    return quiz_question
