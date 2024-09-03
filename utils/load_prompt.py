prompt_for_classification_imdb = f"""
        Hello my good model again. I would like you to classify the comment that I will provide you. 
        The comment is about a IMDB comments for movies.
        I would like you to classify this comment among 2 classes positive and negative. The classes are: 
        positive class: 0
        negative class: 1
        Please keep in mind that the comments are in English. Moreover I will give you some examples on how to decide
        the label of the comment.
        Example comment 1: 
        'This is what happens when a franchise gets lazy, and no one can think of a new twist to add. 
        Remember what happened to the "Childs Play" series? The first three were played as horror films, with genuine 
        scares (albeit predictable) that held true to the theme of the movie. Then they ran out of folks for the doll 
        to stalk, and decided to play it for laughs, with the next two being black comedies.....Well, that;s what 
        happened here, but I think it was not meant to be like that. Kind of like saying, "I WANTED to make 
        pancakes for dessert! I did this on purpose!" when your soufflé accidentally fizzles flat. But the milk was 
        spilled, and it had some value in the theaters as a goof.When the floor ripped out from under the passenger 
        seats, I sort of expected the passengers to extend their legs through the hole, start running Flintstones-Style,
        to safely land the plane in the Alps. I did. It would have fit into the silly campy theme of the rest of the 
        show.Instead of pointing out the obvious physical impossibilities of the film, what about the social 
        implausibilities? Like having George Kennedy's character react calmly to the news that his date was a whore? 
        Even back in 1979, a man would not easily accept the notion that he has just poured his heart out to a paid 
        companion. He supposedly felt he made a connection with a kindred spirit, who is subsequently shown to be a 
        mercenary sex-worker with a come-on line. Who WOULDN'T feel cheated by the experience? And yet he giggles, 
        and wraps his arms around his buddy's waist as they merrily stroll off. What a cheap wrap up of a sleazy scene.
        Ouch.I had an appetite for soufflé, and got served insipid cliché pancakes. And no, you did NOT do it on purpose!'
        Response 1: '1'
        Example comment 2:
        'The greatest Tarzan ever made! This movie is done in a way that no other Tarzan ever has come close in doing. 
        It has every thing in it that you would want in a Tarzan movie. No other Tarzan movie ever has or ever will 
        portray the character this well. I would say that if you have seen a Tarzan movie and liked it you should see 
        this one you will love it, and if you have never seen Tarzan you should see this one and forget the rest 
        of them.'
        Response 2: '0'
        Please provide only the label no more description.
        Here are is the comment for the classification task: + 
        """

prompt_for_classification_airlines = f"""
        Hello my good model again. I would like you to classify the comment that I will provide you. 
        The comment is about a IMDB comments for movies.
        I would like you to classify this comment among 3 classes positive, neutral and negative. The classes are: 
        positive class: 0
        neutral class: 1
        negative class: 2
        Please keep in mind that the comments are in English. Moreover I will give you some examples on how to decide
        the label of the comment.
        Example comment 1: 
        '@SouthwestAir replacing @vitaminwater with beer! Bravo!👏👏 Cheers! 🍻🍻 @Leinenkugels @DosEquis @FatTire'
        Response 1: '0'
        Example comment 2:
        '@SouthwestAir i like to see if i can change flight plz help thx'
        Response 2: '1'
        Example comment 3:
        '@SouthwestAir AH - did DM, no reply. On hold now over 2hrs. Just spent over $1k to get a United flight tmrw to get home. #lame'
        Response 2: '2'
        Example comment 4:
        '@SouthwestAir i hope i can be apart of the team with this job opening!'
        Response 2: '0'
        Example comment 5:
        '@SouthwestAir How can you get your TSA traveler ID added to your boarding pass? Why would it not be included as TSA precheck? Flying tomorrow'
        Response 2: '1'
        Please provide only the label no more description.
        Here are is the comment for the classification task: + 
        """


prompt_for_summarizing_multiple_comments = f"""
    Hello my good model, I would like to create a summary of 300 words for an article and its comments. 
    The article is from the Ministry of Defence and the topic of discussion is: 
    "Ειδικές κατηγορίες αξιωματικών Εκτός Οργανικών Θέσεων". 
    I will provide you the comments and I would like you to create the summary in order the Minister of Defense 
    to be able to comprehend the whole discussion and its most important points. Please I would like the summary
    to be in Greek language as the comments are. Additionaly, I will give you some insights by the exploratory 
    The average word count for the comments is 95 words. Finally, for each comment I have removed special tokens and digits, 
    so be careful with the connections of the words and the meanings. Finally I am going to give you the summaries of the previous
    comments in order to be able to check the history of the previous comments.
    Please write me an efficient summary with all the insights from the comments. Thank you
    Here are the history of the previous summaries of the previous comments: + 
    Here are the comments I would like to create a summary in Greek language: + 
    """

final_prompt_for_summarizing_multiple_comments = f"""
Hello my good model, I would like to create a summary of 600 words about comments for an article by Ministry of Defence.
The article is about Ministry of Defence and the topic of discussion is: "Ειδικές κατηγορίες αξιωματικών Εκτός Οργανικών Θέσεων".
The comments scope to represent the problems, aggrements and/or challenges for the article. However, for the reason that the comments
were too many, I created a summary for each 12 comments of 200 words. So, I would like you to create a final summary 
of 600 words, based on the summaries of the comments. Please write the final summary based on the summaries I am providing you
and the topic. I would like the final summary to be in Greek language as the summaries are.
Here are the summaries: + 

"""


# Function to load the correct prompt
def load_chosen_prompt(name_of_prompt):
    if name_of_prompt == "classification_imdb":
        return prompt_for_classification_imdb
    elif name_of_prompt == "classification_airlines":
        return prompt_for_classification_airlines
    elif name_of_prompt == "summarizing_multiple_comments":
        return prompt_for_summarizing_multiple_comments
    elif name_of_prompt == "final_summarizing_multiple_comments":
        return final_prompt_for_summarizing_multiple_comments
    else:
        raise ValueError(f"Unknown prompt name: {name_of_prompt}")


def get_prompt(prompt, text):
    """
    Construct a complete prompt for a single comment

    :param prompt (str): prompt of our choice.
    :param text (str): The comment for classification or summarization.
    :return (str): Return the complete prompt along with the comment
    """
    # Convert prompt and text to strings to avoid type mismatches
    prompt_str = str(prompt)
    text_str = str(text)
    return prompt_str + text_str


def get_prompt_for_multiple_comments(prompt, comments):
    pass

