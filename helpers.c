#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //Average RGB
    float average_rgb;

    //loop through each pixel
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {

            //Get the average brightness by taking the average of the Red, Green, and Blue values
            average_rgb = ((float) image[h][w].rgbtRed + (float) image[h][w].rgbtBlue + (float) image[h][w].rgbtGreen) / 3;

            //Setting each RBG value to the average value
            image[h][w].rgbtRed = round(average_rgb);
            image[h][w].rgbtBlue = round(average_rgb);
            image[h][w].rgbtGreen = round(average_rgb);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //Temporary Width used for swapping
    int temp_width_R;
    int temp_width_G;
    int temp_width_B;

    //Loop through each pixel
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width / 2; w++)
        {

            //Set the temporary vairble equal to the current pixel
            temp_width_R = image[h][w].rgbtRed;
            temp_width_G = image[h][w].rgbtGreen;
            temp_width_B = image[h][w].rgbtBlue;

            //Set the current pixels equal to their horizontal opposites
            image[h][w].rgbtRed = image[h][(width - 1) - w].rgbtRed;
            image[h][w].rgbtGreen = image[h][(width - 1) - w].rgbtGreen;
            image[h][w].rgbtBlue = image[h][(width - 1) - w].rgbtBlue;

            //Set the horizontal opposites equal to the temporary vairble
            image[h][(width - 1) - w].rgbtRed = temp_width_R;
            image[h][(width - 1) - w].rgbtGreen = temp_width_G;
            image[h][(width - 1) - w].rgbtBlue = temp_width_B;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //Three arrays to hold the blurred values till after the loop
    int dup_image_red[height][width];
    int dup_image_green[height][width];
    int dup_image_blue[height][width];
    //The values used to hold each pixels blurred value during the loop
    float average_red = 0;
    float average_green = 0;
    float average_blue = 0;


//These last vairbles are only changed when a pixel isn't in the middle

    //This the is heights and widths that the blur matrix needs to get input from depending on if a pixel is on a top edge or  right edge or not
    int height2 = -1;
    int width2 = -1;
    //This is the heights and widths the matrix needs to stop at depending if the pixel is on the left or bottom
    int height2_stop = 2;
    int width2_stop = 2;
    //This is a number to determine what you should divide the averages by... usaully it is 9 but in a corner it will be 4 etc...
    int divide_by = 9;


    //Loop through each pixel
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {

            //if the current pixel is the top left pixel
            if ((h == 0) && (w == 0))
            {
                height2 = 0;
                width2 = 0;
                divide_by = 4;
            }
            //if the current pixel is at the top but not in a corner
            else if ((h == 0) && (w != 0) && (w != width - 1))
            {
                height2 = 0;
                divide_by = 6;
            }
            //if the current pixel is at the top and in the far right corner
            else if ((h == 0) && (w == width - 1))
            {
                height2 = 0;
                width2_stop = 1;
                divide_by = 4;
            }
            //If the pixel is on the left but not in a corner
            else if ((h != 0) && (h != height - 1) && (w == 0))
            {
                width2 = 0;
                divide_by = 6;
            }
            //If the pixel is on the far right but not in a corner
            else if ((h != 0) && (h != height - 1) && (w == width - 1))
            {
                width2_stop = 1;
                divide_by = 6;
            }
            //If the pixel is in the bottom right corner
            else if ((h == height - 1) && (w == width - 1))
            {
                height2_stop = 1;
                width2_stop = 1;
                divide_by = 4;
            }
            //If the pixel is in the bottom left corner
            else if ((h == height - 1) && (w == 0))
            {
                height2_stop = 1;
                width2 = 0;
                divide_by = 4;
            }
            //if the pixel is at the bottom and not in a corner
            else if ((h == height - 1) && (w != 0) && (w != width - 1))
            {
                height2_stop = 1;
                divide_by = 6;
            }

            /* -------------------------------------------------------------------- */

            //Finding the rgb values in the surrounding pixels of the [3][3] matrix
            for (int matrix_h = height2; matrix_h < height2_stop; matrix_h++)
            {
                for (int matrix_w = width2; matrix_w < width2_stop; matrix_w++)
                {
                    average_red += (float) image[h + matrix_h][w + matrix_w].rgbtRed;
                    average_green += (float) image[h + matrix_h][w + matrix_w].rgbtGreen;
                    average_blue += (float) image[h + matrix_h][w + matrix_w].rgbtBlue;
                }
            }

            //Averaging them
            average_red /= divide_by;
            average_green /= divide_by;
            average_blue /= divide_by;

            //Changing the current pixels value
            dup_image_red[h][w] = round(average_red);
            dup_image_green[h][w] = round(average_green);
            dup_image_blue[h][w] = round(average_blue);

            /* -------------------------------------------------------------------- */

            //Clearing the averages
            average_red = 0;
            average_green = 0;
            average_blue = 0;

            //Clearing the needed heights and widths
            height2 = -1;
            width2 = -1;
            height2_stop = 2;
            width2_stop = 2;

            //Clearing the thing average is divided by
            divide_by = 9;

        }
    }



    //Loop through each pixel assigning it the proper blurred value
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            //filling the image with blurred values
            image[h][w].rgbtRed = dup_image_red[h][w];
            image[h][w].rgbtGreen = dup_image_green[h][w];
            image[h][w].rgbtBlue = dup_image_blue[h][w];
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    //Three arrays to hold the edge values till after the loop
    int dup_image_red[height][width];
    int dup_image_green[height][width];
    int dup_image_blue[height][width];

    //This the is heights and widths that the blur matrix needs to get input from depending on if a pixel is on a top edge or  right edge or not
    int height2 = -1;
    int width2 = -1;
    //This is the heights and widths the matrix needs to stop at depending if the pixel is on the left or bottom
    int height2_stop = 2;
    int width2_stop = 2;

    //gx and gy
    float Gx[3][3] = { {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };

    float Gy[3][3] = { {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}
    };

    //This will tempororaly hold the multiplied gx and gy values
    float kernal_red_x[3][3];
    float kernal_green_x[3][3];
    float kernal_blue_x[3][3];

    float kernal_red_y[3][3];
    float kernal_green_y[3][3];
    float kernal_blue_y[3][3];

    //This will be all the values from the matrixes above added together by color
    float gx_red = 0;
    float gx_blue = 0;
    float gx_green = 0;

    float gy_red = 0;
    float gy_blue = 0;
    float gy_green = 0;




    //Loop through each pixel
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {

            //if the current pixel is the top left pixel
            if ((h == 0) && (w == 0))
            {
                height2 = 0;
                width2 = 0;
            }
            //if the current pixel is at the top but not in a corner
            else if ((h == 0) && (w != 0) && (w != width - 1))
            {
                height2 = 0;
            }
            //if the current pixel is at the top and in the far right corner
            else if ((h == 0) && (w == width - 1))
            {
                height2 = 0;
                width2_stop = 1;
            }
            //If the pixel is on the left but not in a corner
            else if ((h != 0) && (h != height - 1) && (w == 0))
            {
                width2 = 0;
            }
            //If the pixel is on the far right but not in a corner
            else if ((h != 0) && (h != height - 1) && (w == width - 1))
            {
                width2_stop = 1;
            }
            //If the pixel is in the bottom right corner
            else if ((h == height - 1) && (w == width - 1))
            {
                height2_stop = 1;
                width2_stop = 1;
            }
            //If the pixel is in the bottom left corner
            else if ((h == height - 1) && (w == 0))
            {
                height2_stop = 1;
                width2 = 0;
            }
            //if the pixel is at the bottom and not in a corner
            else if ((h == height - 1) && (w != 0) && (w != width - 1))
            {
                height2_stop = 1;
            }

            /* -------------------------------------------------------------------- */

            //Finding the rgb values in the surrounding pixels of the [3][3] matrix
            for (int matrix_h = height2, i = height2 + 1; matrix_h < height2_stop && i < height2_stop + 1; matrix_h++, i++)
            {
                for (int matrix_w = width2, j = width2 + 1; matrix_w < width2_stop && j < width2_stop + 1; matrix_w++, j++)
                {

                    //Using the gx and gy values to multiply each pixels rgb value
                    kernal_red_x[i][j] =  Gx[i][j] * (float) image[h + matrix_h][w + matrix_w].rgbtRed;
                    kernal_green_x[i][j] = Gx[i][j] * (float) image[h + matrix_h][w + matrix_w].rgbtGreen;
                    kernal_blue_x[i][j] = Gx[i][j] * (float) image[h + matrix_h][w + matrix_w].rgbtBlue;

                    kernal_red_y[i][j] =  Gy[i][j] * (float) image[h + matrix_h][w + matrix_w].rgbtRed;
                    kernal_green_y[i][j] = Gy[i][j] * (float) image[h + matrix_h][w + matrix_w].rgbtGreen;
                    kernal_blue_y[i][j] = Gy[i][j] * (float) image[h + matrix_h][w + matrix_w].rgbtBlue;

                    //Adding up all the previosly multiplied values
                    gx_red += kernal_red_x[i][j];
                    gx_green += kernal_green_x[i][j];
                    gx_blue += kernal_blue_x[i][j];

                    gy_red += kernal_red_y[i][j];
                    gy_green += kernal_green_y[i][j];
                    gy_blue += kernal_blue_y[i][j];
                }
            }

            // Making sure a pixel value isn't over 255
            float red = sqrt((pow(gx_red, 2)) + (pow(gy_red, 2)));
            if (red > 255)
            {
                red = 255;
            }
            float green = sqrt((pow(gx_green, 2)) + (pow(gy_green, 2)));
            if (green > 255)
            {
                green = 255;
            }
            float blue = sqrt((pow(gx_blue, 2)) + (pow(gy_blue, 2)));
            if (blue > 255)
            {
                blue = 255;
            }

            //Changing the current pixels value
            dup_image_red[h][w] = round(red);
            dup_image_green[h][w] = round(green);
            dup_image_blue[h][w] = round(blue);

            /* -------------------------------------------------------------------- */


            //Clearing the needed heights and widths
            height2 = -1;
            width2 = -1;
            height2_stop = 2;
            width2_stop = 2;

            //Clearing each kernal
            for (int i = 0; i < 3; i++)
            {
                for (int j = 0; j < 3; j++)
                {
                    kernal_red_x[i][j] = 0;
                    kernal_green_x[i][j] = 0;
                    kernal_blue_x[i][j] = 0;

                    kernal_red_y[i][j] = 0;
                    kernal_green_y[i][j] = 0;
                    kernal_blue_y[i][j] = 0;
                }
            }

            //Clear each gx rgb value
            gx_red = 0;
            gx_blue = 0;
            gx_green = 0;

            gy_red = 0;
            gy_blue = 0;
            gy_green = 0;

            red = 0;
            green = 0;
            blue = 0;



        }
    }


    //Loop through each pixel assigning it the proper edge value
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            //filling the image with edge values
            image[h][w].rgbtRed = dup_image_red[h][w];
            image[h][w].rgbtGreen = dup_image_green[h][w];
            image[h][w].rgbtBlue = dup_image_blue[h][w];
        }
    }

    return;
}
