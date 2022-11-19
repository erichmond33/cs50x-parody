// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 143091;

// Hash table
node *table[N];
//Head of linked list
node *head[N];

//Size of the dic
unsigned int size_of_dic = 0;




// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //Vairble for the hash index
    unsigned int hash_index;

    //vairble to turn the word into lowercase
    char *word_lower = (char *) word;

    //A curser to parse through the linked list
    node *curser;

    // Hash the word
    hash_index = hash(word_lower);

    //Go to hash_index
    curser = head[hash_index];

    //Loop through the linked list
    while (curser != NULL)
    {
        if (strcasecmp(curser->word, word) == 0)
        {
            return true;
        }
        curser = curser->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    /*The hash function I used is called RSHash from Robert Sedgwicks Algorithms in C book*/
    
    //vairble to turn the word into lowercase
    char *word_lower = (char *) word;
    
    unsigned int b = 378551;
    unsigned int a = 63689;
    unsigned int hash = 0;
    unsigned int i = 0;
    
    for (i = 0; i < strlen(word); word++, i++)
    {
        if (isupper(word_lower[i]))
        {
            word_lower[i] = tolower(word_lower[i]);
            hash = hash * a + (*word);
            a = a * b;
            word_lower[i] = toupper(word_lower[i]);
        }
        else
        {
            hash = hash * a + (*word);
            a = a * b;
        }
    }
    
    hash = hash % 143091;
    
    return hash;

}




// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //Vairble used in fscanf
    char dick_word[LENGTH + 1];

    //Hash index
    int hash_index;

    //Open file
    FILE *dick = fopen(dictionary, "r");
    if (dick != NULL)
    {
        //Read strings
        while ((fscanf(dick, "%s", dick_word)) != EOF)
        {
            //What table we are working with
            hash_index = hash(dick_word);

            //Adding memory to new node
            node *new_node = malloc(sizeof(node));

            //Copying the current word to the new_node
            strcpy(new_node->word, dick_word);

            //Adding an arrow to the first node's value in this list
            new_node->next = head[hash_index];


            //printf("hash table node %s\n", new_node->word);

            //Setting the new node's value equal to the first node in this list
            head[hash_index] = new_node;

            size_of_dic++;
            //printf("\nsize of dic %i\n", size_of_dic);

        }
        fclose(dick);

        //Printing a Linked LIst from an array in the hash table
        /*node *current_node = head[0];
        while (current_node != NULL)
        {
            printf("%s ", current_node->word);
            current_node = current_node->next;
        }*/

        return true;
    }


    return false;
}




// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return size_of_dic;
}





// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    //Vairble for curser
    node *curser;

    //vairble for tmp
    node *tmp;

    // Looping through the hash table
    for (int i = 0; i < N; i++)
    {
        tmp = head[i];
        curser = head[i];

        while (curser != NULL)
        {
            curser = curser->next;

            free(tmp);

            tmp = curser;
        }
    }

    return true;
}
