import pandas as pd
from difflib import get_close_matches
import numpy as np


#For ML-25M (could take upto 2-3 minutes)
"""
r_cols = ['user_id','movieId','rating']
ratings = pd.read_csv(r"ml-25m\ratings.csv",names=r_cols,usecols=range(3),encoding="ISO-8859-1",low_memory=False)
m_cols = ['movieId','title']
movies = pd.read_csv(r"ml-25m\movies.csv",names=m_cols,usecols=range(2),encoding="ISO-8859-1",low_memory=False)
"""

#for ML-100k
r_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv('ml-100k/u.data', sep='\t', names=r_cols, usecols=range(3), encoding="ISO-8859-1")
m_cols = ['movie_id', 'title']
movies = pd.read_csv('ml-100k/u.item', sep='|', names=m_cols, usecols=range(2), encoding="ISO-8859-1")


#creating new frame by merging both tables
ratings = pd.merge(movies, ratings)


#creating new frame with rows of user_id and columns of title--> with values of rating
userRatings = ratings.pivot_table(index=['user_id'],columns=['title'],values='rating')


#creating table of correlation between every movie with atleast 100 users voted for both th
corrMatrix = userRatings.corr(method='pearson', min_periods=100)


#lists only unique elements from the passed list
def unique(list1): 
    unique_list = [] 
    for x in list1:  
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list


#taking input of movies from user
c=1
your_movies=[]
your_ratings=[]
while(c<=3):
    name=input('enter movie title : ')
    temp=get_close_matches(name.capitalize(),ratings['title'])
    for i in ratings['title']:
        if name.lower() in i.lower():
            temp.append(i)
    temp=unique(temp)

    if len(temp)>0:
        for i,j in enumerate(temp):
            print("Press "+str(i)+" for "+str(j))
            last_enum = i


        #check for valid index
        while True:
            try:
                index=int(input("enter the index of movie : "))
            except:
                print('Enter number in range')
            if index < 0 or index > last_enum:
                print("Enter a valid number in range")
                continue
            else:
                break


        # index=int(input("enter the index of movie : "))
        print('\n')
        if temp[index] not in your_movies:
            your_movies.append(temp[index])

            #validate and receive ratings
            while True:
                try:
                    rating=int(input("enter your rating for this movie (0-5) : "))
                except:
                    print('please enter a valid rating')
                    continue
                if rating < 0 or rating>5:
                    print("add rating between 0-5 and try again")
                    continue
                else:
                    break
            your_ratings.append(rating)
            c+=1

        else:
            print('Movie already entered,Try another one')
    else:
        print("No match found,Try Again",'\n')


#adding customs ratings
new_row = pd.DataFrame({your_movies[0]:your_ratings[0], your_movies[1]:your_ratings[1], your_movies[2]:your_ratings[2]},index =[0]) 
userRatings = pd.concat([new_row, userRatings])


#your ratings
myRatings = userRatings.loc[0].dropna()


similarCandidates = pd.Series()
for i in range(0, len(myRatings.index)):
    # retrieve similar movies
    sims = corrMatrix[myRatings.index[i]].dropna()
    # scale or multiply with our rating
    sims = sims.map(lambda x: x * myRatings[i])
    # Add the score to the list of similarity candidates
    similarCandidates = similarCandidates.append(sims)
    

#adding the ratings of same movies recommended by model
similarCandidates = similarCandidates.groupby(similarCandidates.index).sum()


#sort by descending order of correlation
similarCandidates.sort_values(inplace = True, ascending = False)


filteredSims=similarCandidates
#removing our selected movies from the list
for i in myRatings.index:
    try:
        filteredSims=filteredSims.drop(i)
    except:
        continue


#return movies recommended
print("Recommended movies for you : ",'\n')
print(filteredSims.head(10))