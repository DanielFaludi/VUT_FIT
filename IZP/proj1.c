// Daniel Faludi, xfalud00, proj1

#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define BUFFER 4300
#define CHARS_IN_LINE 101
#define WORD 100

void printOutput(char *array, int numberOfHits, char *foundWord, int isOnly)
{
  int i = 0;
  /*
   * If array isn't empty
   */
  if (array && array[0] != 0)
  {
    /*
     * If there is only one match, print the whole word
     */
    if (isOnly)
    {
      printf("Found: %s", foundWord);
      i++;
    }
    /*
     * If the prefix matches more options, print available characters
     */
    else
    {
      /*
       * Sorting output characters alphabetically (Bubble Sort)
       */
      int swapped, count = numberOfHits;
      do
      {
        swapped = 0;
        for (int i = 0; i < count - 1; i++)
        {
          if (array[i] > array[i + 1])
          {
            char c = array[i];
            array[i] = array[i + 1];
            array[i + 1] = c;
            swapped = 1;
          }
        }
        count--;
      } while (swapped);
      /*
       * Print sorted enabled characters
       */
      printf("%s", "Enable: ");
      for (i = 0; i < numberOfHits; i++)
      {
        printf("%c", array[i]);
      }
    }
  }
  /*
   * If there is no match in database, print "Not Found"
   */
  if (array[0] == 0)
  {
    printf("Not found");
  }
  puts("\n");
}

void subSearch(char *subString, char *string)
{
  int i, pos = 0, j = 0, isOnly = 1;
  char foundChars[CHARS_IN_LINE] = {0};
  char foundWord[WORD] = {0};
  /*
   * Checks whether there is a user input
   */
  if (subString[0] != '0')
  {
    /*
     * Iterate until the end of string
     */
    while (string[pos] != 0)
    {
      /*
       * If string character matches the first input character
       */
      if (string[pos] == subString[0])
      {
        i = 1;
        /*
         * Iterate until the end of input and the end of string and until string matches substring
         */
        while (subString[i] != 0 && string[pos + i] != 0 && string[pos + i] == subString[i])
        {
          i++;
        }
        /*
         * If substring on index i is '\0' and string on pos - 1 is new line or '\0'
         */
        if (subString[i] == '\0' && (string[pos - 1] == '\n' || string[pos - 1] == '\0'))
        {
          /*
           * If there are more matches set isOnly flag to 0 and save matches to foundChars
           */
          if (j > 0 && foundChars[0] != string[pos + strlen(subString)])
          {
            isOnly = 0;
          }
          foundChars[j] = string[pos + strlen(subString)];
          j++;
          int l = 0;
          while (string[pos + l] != '\n' && string[pos + l] != '\0')
          {
            l++;
          }
          /*
         * Copies content of a string with a matching prefix (string[pos]) to "foundWord"
         */
          strncpy(foundWord, &string[pos], l + 1);
          foundWord[l] = '\0';
        }
      }
      pos++;
    }
    /*
     * Calls function printOutput
     */
    printOutput(foundChars, j, foundWord, isOnly);
    /*
     * If there is no user input print all starting characters of addresses
     */
  }
  else
  {
    printf("%c", string[0]);
    while (string[pos] != 0)
    {
      if (string[pos - 1] == '\n')
      {
        printf("%c", string[pos]);
      }
      pos++;
    }
    puts("\n");
  }
}

int main(int argc, char *argv[])
{
  int i = 0, c = 0;
  char array[BUFFER];
  int charsInLine = 0;

  /*
   * Feed database from stdin to "array" and check for length of addresses in database 
   */
  while ((c = getchar()) != EOF && c != '0')
  {
    array[i] = toupper(c);
    charsInLine++;
    if (charsInLine >= CHARS_IN_LINE)
    {
      fprintf(stderr, "Error: Address in database can't be over 100 characters long.");
      puts("\n");
      return -1;
    }
    else if (c == '\n')
    {
      charsInLine = 0;
    }
    i++;
  }

  /*
   * Assign user input argv[1] in to "input" variable in uppercase and check for entered address length
   */
  char *input = {"0"};
  if (argc == 2)
  {
    input = argv[1];
    for (int i = 0; input[i] != '\0'; i++)
    {
      input[i] = toupper(input[i]);
      charsInLine++;
      if (charsInLine >= WORD)
      {
        fprintf(stderr, "Error: Entered address can't be over 100 characters long.");
        puts("\n");
        return -1;
      }
    }
  }

  /*
   * Calls function subSearch
   */
  subSearch(input, array);
  return 0;
}
