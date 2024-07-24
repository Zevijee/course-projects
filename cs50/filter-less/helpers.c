#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            float sum = (red + blue + green)/ 3.0;
            sum = round(sum);
            image[i][j].rgbtRed = sum;
            image[i][j].rgbtBlue = sum;
            image[i][j].rgbtGreen = sum;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
        for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            int Red = round(red * .393 + green * .769 + blue * .189);
            if (Red > 255)
            {
                Red = 255;
            }
            int Green = round(red * .349 + green * .686 + blue * .168);
            if (Green > 255)
            {
                Green = 255;
            }
            int Blue = round(red * .272 + green * .534 + blue * .131);
            if (Blue > 255)
            {
                Blue = 255;
            }
            image[i][j].rgbtRed = Red;
            image[i][j].rgbtBlue = Blue;
            image[i][j].rgbtGreen = Green;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0, x = width / 2; j < x; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    int t_red;
    int t_green;
    int t_blue;
    float counter;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            t_red = 0;
            t_green = 0;
            t_blue = 0;
            counter = 0.00;
            // now go through each surrounding pixel
            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    if (i + x < 0 || j + y < 0 || i + x >= height || j + y >+ width)
                    {
                        continue;
                    }
                    t_red = image[i + x][j + y].rgbtRed + t_red;
                    t_green = image[i + x][j + y].rgbtGreen + t_green;
                    t_blue = image[i + x][j + y].rgbtBlue + t_blue;
                    counter++;
                }
            }
            temp[i][j].rgbtRed = round((double)t_red / (double)counter);
            temp[i][j].rgbtGreen = round((double)t_green / (double)counter);
            temp[i][j].rgbtBlue = round((double)t_blue / (double)counter);
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
        }
    }
}
