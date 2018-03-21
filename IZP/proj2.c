// Daniel Faludi, xfalud00, IZP proj2
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>

// Defined constants
#define COEFF 13
#define IMPLICIT_HEIGHT 1.5
#define IMPLICIT_TAN_ITERATIONS 10

// Function prototypes
double parseDouble(const char *str);
long parseLong(const char *str);
double taylor_tan(double x, unsigned int n);
double cfrac_tan(double x, unsigned int n);
double obj_distance(double x, double height);
double obj_height(double x, double y, double height);
int printTan(char *argv[]);
int printHeightDist(int argc, char *argv[]);
void help();

int main(int argc, char *argv[])
{
	// If there are less than two arguments print error and return -1
	if (argc < 2)
	{
		fprintf(stderr, "Error: no arguments, try '--help'");
		puts("\n");
		return -1;
	}

	// Calls function help() if '--help' is entered or an error if the argument is invalid
	if (argc == 2)
	{
		if (strcmp(argv[1], "--help") == 0)
		{
			help();
		}
		else
		{
			fprintf(stderr, "Error: '%s' is incorrect or incomplete argument, try '--help'", argv[1]);
			puts("\n");
			return -1;
		}
	}

	// Calls function printHeightDist if one condition is met
	if (argc == 3 || argc == 4 || argc == 5 || argc == 6)
	{
		if (strcmp(argv[1], "-c") == 0 || strcmp(argv[1], "-m") == 0)
		{
			printHeightDist(argc, argv);
		}
		if (strcmp(argv[1], "--tan") == 0)
		{
			printTan(argv);
		}
	}

	// Prints an error if there are more than 6 arguments
	if (argc > 6)
	{
		fprintf(stderr, "Error: too many arguments, try '--help'");
		puts("\n");
		return -1;
	}

	return 0;
}

// strtod function with error checking
double parseDouble(const char *str)
{
	double val = 0;
	char *endptr;

	val = strtod(str, &endptr);

	if (*endptr != '\0')
	{
		fprintf(stderr, "Error: strtod conversion was unsuccessful, leftover string is %s", endptr);
		puts("\n");
		exit(EXIT_FAILURE);
	}
	else
	{
		return val;
	}
}

// strtol function (base 10) with error checking
long parseLong(const char *str)
{
	long val = 0;
	char *endptr;

	val = strtol(str, &endptr, 10);
	if (*endptr != '\0')
	{
		fprintf(stderr, "Error: strtol conversion was unsuccessful, leftover string is %s", endptr);
		puts("\n");
		exit(EXIT_FAILURE);
	}
	else
	{
		return val;
	}
}

// Calculates tangent approximation based on taylor polynomials
double taylor_tan(double x, unsigned int n)
{
	unsigned int i;
	// Coefficients
	double nom[COEFF] = {1.0, 1.0, 2.0, 17.0, 62.0, 1382.0, 21844.0, 929569.0, 6404582.0, 443861162.0,
											 18888466084.0, 113927491862.0, 58870668456604.0};
	double denom[COEFF] = {1.0, 3.0, 15.0, 315.0, 2835.0, 155925.0, 6081075.0, 638512875.0, 10854718875.0, 1856156927625.0, 194896477400625.0,
												 49308808782358125.0, 3698160658676859375.0};

	double res = 0.0;
	double power = x * x;

	// Update res based on the current iteration
	for (i = 0; i < n; i++)
	{
		res += (x * nom[i]) / denom[i];
		x *= power;
	}

	//Returns result
	return res;
}

// Calculates tangent approximation based on continued fraction
double cfrac_tan(double x, unsigned int n)
{
	double power = x * x;
	double res = (n * 2 - 1) - (power);
	unsigned int i;

	//Update res based on current iteration
	for (i = n - 1; i > 0; i--)
	{
		res = (i * 2 - 1) - (power / res);
	}

	// Return x divided by res
	return (x / res);
}

// Calculates the object distance using our cfrac_tan function
double obj_distance(double x, double height)
{
	double res = height / cfrac_tan(x, IMPLICIT_TAN_ITERATIONS);
	return res;
}

// Calculates the height of an object using our obj_distance and cfrac_tan functions
double obj_height(double x, double y, double height)
{
	double res = obj_distance(x, height) * cfrac_tan(y, IMPLICIT_TAN_ITERATIONS) + height;
	return res;
}

// Prints both tangent functions results based on user specified interval
int printTan(char *argv[])
{
	double angle, tayRes, cfRes, tayDiff, cfDiff;
	int n, m;

	// If the first argument is '--tan'
	if (strcmp(argv[1], "--tan") == 0)
	{
		angle = parseDouble(argv[2]);
		if (angle <= 0 || angle > 1.4)
		{
			printf("Error: wrong angle value, usage: [0 < ANGLE <= 1.4 < PI/2]");
			puts("\n");
			return -1;
		}
		m = parseLong(argv[3]);
		n = parseLong(argv[4]);

		// Prints error if a wrong interval is entered
		if (m > n || n > 13 || m < 1)
		{
			fprintf(stderr, "Error: wrong interval, usage: [0 < N <= M < 14]");
			puts("\n");
			return -1;
		}

		// Prints all required elements based on current iteration
		while (m <= n)
		{
			tayRes = taylor_tan(angle, m);
			cfRes = cfrac_tan(angle, m);
			tayDiff = tan(angle) - tayRes;
			cfDiff = tan(angle) - cfRes;
			printf("%d %e %e %e %e %e\n", m, tan(angle), tayRes, fabs(tayDiff), cfRes, fabs(cfDiff));
			m++;
		}
	}

	// Prints an error if a wrong argument is entered
	else
	{
		fprintf(stderr, "Error: wrong argument, try '--help'");
		puts("\n");
		return -1;
	}
	return 0;
}

int printHeightDist(int argc, char *argv[])
{
	double alpha = 0.0, beta = 0.0, height = IMPLICIT_HEIGHT;

	// If the conditions are met
	if (argc == 3 || argc == 4 || argc == 5 || argc == 6)
	{
		// if -c argument is entered, set height
		if (strcmp(argv[1], "-c") == 0 && strcmp(argv[3], "-m") == 0)
		{
			height = parseDouble(argv[2]);

			// Prints an error if wrong height value is entered
			if (height > 100)
			{
				fprintf(stderr, "Error: wrong height value, usage: [0 < HEIGHT <= 100]");
				puts("\n");
				return -1;
			}

			// Set one angle and print object distance	
			if (argc == 5)
			{
				alpha = parseDouble(argv[4]);
				// Prints an error if incorrect angle value is entered
				if (alpha <= 0 || alpha > 1.4)
				{
					fprintf(stderr, "Error: wrong angle value, usage: [0 < ANGLE <= 1.4 < PI/2]");
					puts("\n");
					return -1;
				}
				printf("%.10e\n", obj_distance(alpha, height));
			}

			// Set both angles, print object distance and height
			if (argc == 6)
			{
				alpha = parseDouble(argv[4]);
				beta = parseDouble(argv[5]);
				// Prints an error if incorrect angle value is entered
				if (alpha <= 0 || alpha > 1.4 || beta <= 0 || beta > 1.4)
				{
					fprintf(stderr, "Error: wrong angle value, usage: [0 < ANGLE <= 1.4 < PI/2]");
					puts("\n");
					return -1;
				}
				printf("%.10e\n", obj_distance(alpha, height));
				printf("%.10e\n", obj_height(alpha, beta, height));
			}
		}

		// If only -m argument is entered, calculate distance and height using implicit sensor height
		else if (strcmp(argv[1], "-m") == 0)
		{
			alpha = parseDouble(argv[2]);
			if (alpha <= 0 || alpha > 1.4)
				{
					fprintf(stderr, "Error: wrong angle value, usage: [0 < ANGLE <= 1.4 < PI/2]");
					puts("\n");
					return -1;
				}
			printf("%.10e\n", obj_distance(alpha, height));

			// Sets second angle if it is entered
			if (argc == 4)
			{
				beta = parseDouble(argv[3]);
				if (beta <= 0 || beta > 1.4)
				{
					fprintf(stderr, "Error: wrong angle value, usage: [0 < ANGLE <= 1.4 < PI/2]");
					puts("\n");
					return -1;
				}
				printf("%.10e\n", obj_height(alpha, beta, height));
			}
			return 0;
		}

		// Print error if wrong arguments are entered
		else
		{
			fprintf(stderr, "Error: wrong or incomplete arguments, try '--help");
			puts("\n");
			return -1;
		}
	}
	return 0;
}

// Prints help
void help()
{
	// Basic info
	printf("This program calculates tangent approximations (in radians) based on taylor polynomials and continued fractions, ");
	printf("It also calculates a distance and/or height of an object based on sensor height and tangent approximations.\n\n");

	// --tan help
	printf("--tan ANGLE M N\t\tPrint tangent approximations\nusage: (0 < ANGLE <= 1.4) (0 < N <= M < 14)\n\n");

	// -m help
	printf("-m ANGLE1 [ANGLE2]\tPrint height and distance of an object if both angles are entered, ");
	printf("or only distance if only one angle is entered\nusage: (0 < ANGLE <= 1.4)\n\n");

	// -c -m help
	printf("-c X -m ANGLE1 [ANGLE2]\tPrint height and distance of an object with non-implicit sensor height\n");
	printf("usage: (0 < X <= 100) (0 < ANGLE <= 1.4)\n\n");
}
