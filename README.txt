===AUTHORS===
Shehroze Khan (ccid: shehroze) and Afia Anjum (ccid: afia)

===SOURCES===
1. https://www.rexegg.com/regex-quickstart.html (REGEX CHEAT SHEET)
2. https://stackabuse.com/using-regex-for-text-manipulation-in-python/ (USEFUL SYNTAX GUIDE FOR REGEX LIBRARY IN PYTHON)
3. https://www.nltk.org/api/nltk.tokenize.html (UNDERSTANDING THE NLTK TOKENIZE API)
4. https://riptutorial.com/python/example/26946/writing-a-tsv-file (WRITING A TSV FILE)
5. https://stackoverflow.com/questions/18262293/how-to-open-every-file-in-a-folder (TO OPEN ALL FILES IN THE DIRECTORY)
6. https://docs.python.org/3/library/re.html
7. https://www.geeksforgeeks.org/regular-expression-python-examples-set-1/
8. https://www.datacamp.com/community/tutorials/python-regular-expression-tutorial

===EXECUTION INSTRUCTIONS===
Place the python file in the directory containing all the wiki files. Run the python file on the terminal without any arguments. The corresponding tsv files will be generated in the same directory.

===DESIGN DECISIONS===
We separate the InfoBox from the rest of the body text in the wiki file and extract facts from these separately.

To extract facts from the infobox, we first tokenize our text into sentences. Next, we loop through these sentences one by one to extract the following facts about the movie:

1.DIRECTOR
The program is able to extract one or multiple names of the directors of a movie
2.PRODUCER
The program is able to extract one or multiple names of the producers of a movie
3.WRITER
The program is able to extract one or multiple names of the writers of a movie
4.STARRING
The program is able to extract one or multiple names of the casts of a movie
5.MUSIC
The program is able to extract one or multiple names of the music composers of a movie
6.CINEMATOGRAPHY
The program is able to extract one or multiple names of the cinematographer of a movie
7.EDITING
The program is able to extract one or multiple names of the editors of a movie
8.STUDIO
The program is able to extract one or multiple names of the studio under which a movie got released
9.RELEASED DATE
The program is able to extract the date on which the movie got released
10.RUNTIME
The program is able to extract the runtime of a movie in minutes
11.LANGUAGE
The program is able to extract the language of a movie
12.BUDGET
The program is able to extract the budget(in USD or ¥) for a movie
13.GROSS
The program is able to extract the gross income(in USD or ¥) of a movie

To extract facts from the body text, we first tokenize our text into sentences using the nltk library, storing these in a list. Next, we loop through these sentences one by one to extract the following facts about the movie:

1. RELEASE YEAR
This information is almost always found in the first sentence of the body text of the form "{{movie_name}} is a {{movie_year}} {{movie_nationality}} {{genre1}} film..." We define a function extract_movie_year that takes in this sentence and extracts and outputs the year as a string.

2. GENRES
The genre or film category information is also almost always found in the first sentence of the body text. We define a funtion extract_movie_genres, which first splits the sentence by the movie year in order to isolate the second part of the sentence, i.e. "{{movie_nationality}} {{genre1}} film {{action_verb(s)}} by..."

Next, we further split this isolated sentence by the word "by" in order to isolate the genre part of the sentence. The reason we follow this strategy is because the genre information is contained in the double square brackets as part of the metadata of the wiki file, as is information about the directors, production stuff, writers, etcetera.

In order to separate the latter from the former, therefore, we further split by the word "by", since the latter information is almost always captured in the passive voice (e.g. film written/directed/produced by... [[name]] ).

Once we isolate the genres from the sentence, we write regex to extract information from inside these square brackets and collect it in a list.

3. ROTTEN TOMATOES APPROVAL RATING
This fact is almost always found in the first sentence of the body text following the "critical response" subsection of the wiki file. The sentence is almost always of the form "{{movie_name}} received an approval rating of {{percentage}}% ... {{number_of_reviews}} critics/reviews ..." Accordingly, we write a function extract_rt_approval_rating to extract the percentage value depicting the rotten tomatoes approval rating.

4. ROTTEN TOMATOES REVIEWS
This fact, similar to the previous one, is also found in the same sentence. We write the function extract_rt_reviews to extract the number of reviews from the sentence, which caters for the two cases in which the sentence mentions the review number, which are "X reviews" or "X critics" where X is the number we try to extract.

In order to ouput our results in a tsv file, we use Python's csv module. We collect all of our results in a giant list comprising small lists of 4 elements each. We write a function generate_tsv that takes in this list of lists as input, loops through it, writing the small lists to the output file.