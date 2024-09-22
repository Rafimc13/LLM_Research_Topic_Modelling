# define the prompt templates
prompts_dict = {
    'prompt_for_classification_imdb':
        """
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
        Here are is the comment for the classification task: {comment}
        """,
    'prompt_for_classification_airlines':
    """
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
        Here are is the comment for the classification task: {comment}
    """,
    'prompt_for_summarizing_multiple_comments':
    """
    Hello my good model, I would like to create a summary for a group of comments. Please consider the length
    of the summary based on the insights of the comments. Try not to repeat similar topics. The language of the comments
    is {language} and the topic of discussion is: {topic} 
    I will provide you the comments and I would like you to create the summary in order a to be able to get the most
    important topics and insights of these comments. Finally I am going to give you summaries of the previous groups of
    comments of the same topic discussion, in order to be able to use similar structure.
    Please write me an efficient summary with all the insights from the comments. Please write only the 
    summary and do not add anything else. Thank you.
    Here are the history of the previous summaries of the previous groups of comments: {previous_summaries}
    Here are the comments I would like to create a summary: {comments}
    """,
    'final_prompt_for_summarizing_multiple_comments':
    """
    Hello my good model, I would like to create a final summary by derived summaries about the following topic discussion:
    {topic}. The comments scope to represent the problems, agreements and/or challenges of the topic discussion. 
    However, for the reason that the comments were too many, I created a summary for groups of comments. So, I would like
    you to create a final summary based on these summaries of the comments. Please consider the length
    of the summary based on the insights of the summaries. Try not to repeat similar topics. Please write only the 
    summary and do not add anything else. Thank you.
    Here are the summaries: {summaries} 
    """,
    'prompt_for_classification_QMSUM':
    """
        Hello my good model. I would like you to classify the comment that I will provide you. 
        The comment is about a Meeting of a company for products.
        I would like you to classify this comment among 3 classes positive, neutral and negative. The classes are: 
        positive class: 0
        neutral class: 1
        negative class: 2
        Please keep in mind that the comments are in English. Moreover I will give you some examples on how to decide
        the label of the comment.
        Example comment 1: 
        Um thank you for that . Uh Craig do you wanna?
        Response 1: '0'
        Example comment 2:
        Is it working ?
        Response 2: '1'
        Example comment 3:
        Mm . Not quite .
        Response 2: '2'
        Please provide only the label no more description.
        Here are is the comment for the classification task: {comment}
    """,
    'prompt_for_topic_extraction':
    """
    Hello my good model. I would like you to implement a topic extractions, in the comment that I will provide you. 
    The discussion of the comment is about: "{topic}" and the language of the comment is {language}. Please think about 
    your answer and create topics as more accurate as possible. Moreover, I will provide you with the lists of extracted
    topics for some previous comments. Please write only the list of extracted topics and not anything else. Here is an 
    example of the format of your response:
    Extracted topics: ['topic1', 'topic2', ... etc]
    Here are the previous extracted topics: {topics} 
    Here is the comment: {comment}  
    """
}

# Define the required arguments for each prompt
required_args = {
    "prompt_for_classification_imdb": ["comment"],
    "prompt_for_classification_airlines": ["comment"],
    "prompt_for_summarizing_multiple_comments": ["language", "topic", "previous_summaries", "comments"],
    "final_prompt_for_summarizing_multiple_comments": ["topic", "summaries"],
    "prompt_for_classification_QMSUM": ["comment"],
    "prompt_for_topic_extraction": ["topic", "language", "topics", "comment"]
}


def load_chosen_prompt(prompt_name):
    """
    Load the selected prompt based on the name of the prompt and print details about its required arguments.

    Args:
        prompt_name (str): The name of the prompt to load.

    Returns:
        str: The corresponding prompt template for the given prompt name.
        """
    try:
        if 'classification' in prompt_name:
            return prompts_dict[prompt_name]
        else:
            print(f'The number of arguments to contain in the prompt are: {len(required_args[prompt_name])}')
            print(f'The required arguments are: {required_args[prompt_name]}')
            return prompts_dict[prompt_name]
    except KeyError:
        raise ValueError(f"Unknown prompt name: {prompt_name}")


def get_final_prompt(prompt, **kwargs):
    """
    Generate a complete prompt by replacing the placeholders in the prompt template with the provided arguments.

    Args:
        prompt (str): The prompt template containing placeholders.
        kwargs: Arbitrary keyword arguments. These are the key-value pairs that will be used
                to replace the placeholders in the prompt template.

    Returns:
        str: A complete prompt with all placeholders filled using the provided keyword arguments.
        """
    # Fill the placeholders in the template with the provided keyword arguments
    try:
        return prompt.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing required argument for placeholder: {e}")

