import nltk
import re
import csv
import os
import glob

#=====functions needed to process the information box======

#this function will replace anything that is between <ref>--</ref> including citations with an empty space ("")
def stripref(data):
    p = re.compile(r'<.*?>({{cite.*?}}<.*?>)?')
    return p.sub('', data)

#this function will replace any urls mentioned in the text with an empty space ("")
def stripurl(data):
    p= re.compile(r'https?:\/\/.*?\/.*?\/')
    return p.sub('',data)

#this function will replace any nobackspace character followed by a semicolon mentioned in the text with an empty space ("")
def stripnbsp1(data):
    p= re.compile(r'&nbsp;')
    return p.sub(' ',data)

#this function will replace any nobackspace character along with curly braces mentioned in the text with an empty space ("")
def stripnbsp2(data):
    p= re.compile(r'{{nbsp}}')
    return p.sub(' ',data)

#this function will replace any whitespace character followed by closing curly braces mentioned in the infobox 
#part with only the closing curly braces
def infoboxmakeline(data):
    p= re.compile(r'[ \t\r]}}')
    return p.sub('}}\n',data)
        
#this function will replace any whitespace character followed by a pipe mentioned in the infobox part with a newline and the pipe  
def infoboxmakeline2(data):
    q= re.compile(r'[ \t\r]\|')
    return q.sub('\n|',data)

#this function will convert any strings to a list and putting a newline after each of the elements of the list. 
#This is done to traverse each line of the text part one by one  
def convert_str_to_list(string): 
    li = list(string.split("\n")) 
    return li 


#======functions needed for processing textbody======

def extract_movie_year(s):
	m = re.search(r"\b\d{4}\b", s)
	return m.group(0) if m is not None else ""

## Takes a sentence s, and extracts all its genres / categories as described in the article ##
def extract_genres(s):
	tmp_s = re.split(r"\b\d{4}\b", s)[1].strip() # split sentence by movie year to create tmp_s
	new_s = re.split(r"[\w\s]+by", tmp_s)[0]	 # split tmp_s by "by" to isolate phrase containing genre info

	m = re.findall(r"\[\[[\w|\s|\-|\|]+\]\]", new_s) # finding all the genres in Wikipedia's double-square brackets markup

	if m is not None:
		genres = [] # this stores all the extracted genres
		for genre in m:
			g = re.sub(r"\[|\]", "", genre).split('|')[0] # cleaning up the extracted genres
			genres.append(g)

		return genres
	else:
		return []

## Takes a sentence s, and extracts a percentage value depicting movie approval rating on Rotten Tomatoes ##
def extract_rt_approval_rating(s):
	m = re.search(r"\d{1,3}%", s) # regex to extract percentage value

	return m.group(0) if m is not None else ""

## Takes a sentence s, and extracts the number of reviews from critics on Rotten Tomatoes ##
def extract_rt_reviews(s):
	m = re.search(r"\d+\s(critics|reviews)", s) # extracting "X critics" or "X reviews" where X is the number of reviews
	return m.group(0).split(" ")[0] if m is not None else ""

## Takes in the movie name and the list of facts and creates an output tsv file, movie_name.tsv  ##
def generate_tsv(movie_name, facts_list):
	file_name = movie_name + ".tsv"
	with open(file_name, 'wt', encoding='utf8') as out_file:
		tsv_writer = csv.writer(out_file, delimiter='\t')
		tsv_writer.writerow(['Subject', 'Predicate', 'Object', 'Evidence'])
		for fact in facts_list:
			tsv_writer.writerow(fact)

def main():
    for filename in glob.glob('*.wiki'):
        #print(filename)
        myfile = open(filename, encoding="utf8")
        #this portion of the code opens a file, read from that and keeps entire portion of the file as a string
        #myfile = open("D:\ALBERTA\Fall 2019\Intro to NLP\Assignment 1\A1\Antz.wiki", encoding="utf8")
        article= myfile.read()
            
        #The string named article contains many new lines. This block of code removes all the new lines and replace it with empty space. 
        #It also divides the entire portion of the text into two parts(info box and the text body) running multiple regular expressions. 
        article_text = re.sub('\n', ' ', article)
        info=re.search('{{Infobox.*?(\'){5}',article_text).group()
        finalinfobox=re.search('.*}}',info).group()
        textpart=re.search('(\'){5}.*$',article_text).group()
        
        #to extract the name of the movie
        moviename=re.search('(\'){5}.*?(\'){5}',article).group()
        moviename=moviename.strip('(\'){5}')
        
        #Having divided the entire text into two parts, it strips out all of the references from both the parts(infobox_part and textpart)
        finalinfobox=stripref(finalinfobox)
        textpart=stripref(textpart)
        
        
        ####FOR PROCESSING INFO BOX OF THE MOVIES
        
        #Having divided the entire text into two parts, it strips out all of the url sections from both the parts(infobox_part and textpart)
        finalinfobox=stripurl(finalinfobox)
        textpart=stripurl(textpart)
        
        #This portion strips out all of the nbsp portions from the infobox_part
        finalinfobox=stripnbsp1(finalinfobox)
        finalinfobox=stripnbsp2(finalinfobox)
        
        #These two lines makes our infobox easier to traverse and extract information accordingly.
        #In other words, these lines help us by putting every information that we need to extract regarding a certain field in each of the single line.
        finalinfobox=infoboxmakeline(finalinfobox)
        finalinfobox=infoboxmakeline2(finalinfobox)
        
        #For the information extraction purpose, we converted our infobox portion into a list 
        #so that we can traverse each of the line and run regular expression over it. 
        infoboxList=convert_str_to_list(finalinfobox)
        
        
        #This portion is used to define some of the lists and strings that we need in the next part of the program
        #defining all of these are important to avoid the cases when a particular pattern(regular expression) is not present in a file 
        
        mo=[]
        mo1=[]
        mo2=[]
        mo3=[]
        mo4=[]
        mo5=[]
        temp1=[]
        temp2=[]
        temp3=[]
        temp4=[]
        temp5=[]
        temp6=[]
        temp7=[]
        temp8=[]
        temp9=[]
        temp10=[]
        temp11=[]
        movie_budget=""
        movie_gross=""
        evidence1=""
        evidence2=""
        evidence3=""
        evidence4=""
        evidence5=""
        evidence6=""
        evidence7=""
        evidence8=""
        evidence9=""
        evidence10=""
        evidence11=""
        evidence12=""
        evidence13=""

        # A loop to traverse the entire list1 that contains only the info box portion
        for line in infoboxList:
                
            #This portion looks up for some of the relation that we are trying to extract like the director, writer, etc...            
            ko=re.findall('director',line)
            ko1=re.findall('producer',line)
            ko2=re.findall('writer',line)
            ko3=re.findall('starring',line)
            ko4=re.findall('music',line)
            ko5=re.findall('cinematography',line)
            ko6=re.findall('editing',line)
            ko7=re.findall('studio',line)
            ko8=re.findall('released',line)
            ko9=re.findall('runtime',line)
            ko10=re.findall('language',line)
            ko11=re.findall('budget',line)
            ko12=re.findall('gross',line)
            ko13=re.findall('production companies',line)
            
            #this portion searches for similar patterns inside each of the line
            mo = re.findall("\[\[.*?\]\]", line)
            mo1 = re.findall("(\d{4}\|\d{1,2}\|\d{1,2})", line)
            mo2 = re.findall("\d{1,} minutes?", line)
            mo3 = re.findall('[\$\¥]?\|?[0-9]+\.?[0-9]+ [mb]illion', line)
            mo4 = re.findall('language[ \t\r]*\=[ \t\r]*[A-Za-z]*', line)
            #The next portion of the code is built up using an and inside the if statement, 
            #which suggests that if a 'relation' word is found and a particular pattern matches, 
            #then it is going to extract all the information from that line and append it to a single string. 
            if(mo and ko):
                for i in mo:
                    i=i.strip('[[')
                    i=i.strip(']]')
                    temp1.append(i)
                    evidence1=line
                
            if(mo and ko1):
                for i in mo:
                    i=i.strip('[[')
                    i=i.strip(']]')
                    temp2.append(i)
                    evidence2=line
                
            if(mo and ko2):
                for i in mo:
                    i=i.strip('[[')
                    i=i.strip(']]')
                    temp3.append(i) 
                    evidence3=line

            if(mo and ko3):
                for i in mo:
                    i=i.strip('[[')
                    i=i.strip(']]')
                    temp4.append(i) 
                    evidence4=line
        
            if(mo and ko4):
                for i in mo:
                    i=i.strip('[[')
                    i=i.strip(']]')
                    temp5.append(i) 
                    evidence5=line
        
            if(mo and ko5):
                for i in mo:
                    i=i.strip('[[')
                    i=i.strip(']]')
                    temp6.append(i)   
                    evidence6=line
        
            if(mo and ko6):
                for i in mo:
                    i=i.strip('[[')
                    i=i.strip(']]')
                    temp7.append(i)    
                    evidence7=line
        
            if(mo and (ko7 or ko13)):
                for i in mo:
                    i=i.strip('[[')
                    i=i.strip(']]')
                    temp8.append(i) 
                    evidence8=line
                
            if(mo1):
                evidence9=line
                released_date=mo1[0]
              
            if(mo2):
                run_time=mo2[0]
                evidence10=line
              
            if(mo4):
                for i in mo4:
                    i=i.strip('language = ')
                    temp9.append(i)
                    evidence11=line

            if(mo3 and ko11):
                mo3[0]=mo3[0].replace("|", "")
                movie_budget=mo3[0]
                for i in mo3:
                    temp10.append(i)
                    evidence12=line
                
        
            if(mo3 and ko12):
                movie_gross=mo3[0].replace("|", "")
                evidence13=line
                
    
    
    
    #####FOR PROCESSING TEXT PART OF THE MOVIE
    
        
        
        body = textpart
        
    
        tokens = nltk.sent_tokenize(body)
    
        list_of_facts = [] # List of list of facts
    
        s1 = tokens[0] # movie year and genre evidence
        
        # Extracting the director
        for i in range(len(temp1)):
            list_of_facts.append([moviename, 'director', temp1[i], evidence1])
           
        # Extracting the producer
        for i in range(len(temp2)):
            list_of_facts.append([moviename, 'producer', temp2[i], evidence2])
       
       # Extracting the writer
        for i in range(len(temp3)):
            list_of_facts.append([moviename,'writer',temp3[i], evidence3])
       
        # Extracting the starring
        for i in range(len(temp4)):
            list_of_facts.append([moviename,'starring',temp4[i], evidence4])
           
        # Extracting the music
        for i in range(len(temp5)):
            list_of_facts.append([moviename,'music',temp5[i], evidence5])
        
        # Extracting the cinematography
        for i in range(len(temp6)):
            list_of_facts.append([moviename,'cinematography',temp6[i], evidence6])
           
       # Extracting the editing
        for i in range(len(temp7)):
            list_of_facts.append([moviename,'editing',temp7[i], evidence7])
            
       # Extracting the studio
        for i in range(len(temp8)):
            list_of_facts.append([moviename,'studio',temp8[i], evidence8])
       
        list_of_facts.append([moviename,'released date',released_date, evidence9])
        list_of_facts.append([moviename,'run time',run_time, evidence10])
        if len(temp9) > 0:
            list_of_facts.append([moviename,'language',temp9[0], evidence11])
        list_of_facts.append([moviename,'budget',movie_budget, evidence12])
        list_of_facts.append([moviename,'gross',movie_gross, evidence13])
    
    	# Extracting the movie year
        movie_year = extract_movie_year(s1)
        list_of_facts.append([moviename, 'year', movie_year, s1])
    
    	# Extracting the genres
        if movie_year:
            genres = extract_genres(s1)
            for g in genres:
                list_of_facts.append([moviename, 'genre', g, s1])
       
    	# Extracting Rotten Tomatoes rating and review information
        for s in tokens:
            if re.search(r"Critical response", s) is not None:
                rt_rating = extract_rt_approval_rating(s)
                list_of_facts.append([moviename, 'approvalRating', rt_rating, s])
    
                rt_reviews = extract_rt_reviews(s)
                list_of_facts.append([moviename, 'reviews', rt_reviews, s])
                
    
        ## outputting facts 
        generate_tsv(moviename, list_of_facts) # Create the output tsv file

main()







    


















