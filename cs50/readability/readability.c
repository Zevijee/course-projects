#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

double Letters(string text);
double Words(string text);
double Sentences(string text);
double Index(double l, double s, double w);

int main(void)
{
    string user_input = get_string("Text: ");
    double l = Letters(user_input);
    double w = Words(user_input);
    double s = Sentences(user_input);
    int I = round(Index(l, s, w));
    if (I < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (I > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", I);
    }
}

double Letters(string text)
{
    double C = 0;
    for (int i = 0; i < (int)strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            C++;
        }
    }
    return C;
}

double Words(string text)
{
    double C = 1;
    for (int i = 0; i < (int)strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            C++;
        }
    }
    return C;
}

double Sentences(string text)
{
    double C = 0;
    for (int i = 0; i < (int)strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        C++;
    }
    return C;
}

double Index(double l, double s, double w)
{
    double index = (0.0588 * l / w * 100) - (0.296 * s / w * 100) - 15.8;
    return index;
}