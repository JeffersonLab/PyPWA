#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
#include <complex.h>
#include <time.h>
//Second attempt at remaking likelihood function using Igor amplitudes, with filereading



complex double igor_amplitude(double s, double t, double u, double p)
{
	//printf("in the igor function\r\n");
	complex double ret;
	complex double res = 0.0;
	dummy_(&res);
	//printf("dummy finished\r\n");
	amp_(&res,&s,&t,&u,&p);	
	//printf("amp finished\r\n");
	return ret;
}


double dtime()
{
double tseconds = 0.0;
struct timeval mytime;
gettimeofday(&mytime,(struct timezone*)0);
tseconds = (double)(mytime.tv_sec + mytime.tv_usec*1.0e-6);
return( tseconds );
}

#define FLOPS_ARRAY_SIZE 137137 //
#define MAXFLOPS_ITERS 100000
#define LOOP_COUNT 128
#define FLOPSPERCALC 2

complex double A[FLOPS_ARRAY_SIZE]__attribute__((aligned(64)));

complex double lnl(complex double A[])
{
double sum = 0;
int x;
int numthreads;

omp_set_num_threads(122);
kmp_set_defaults("KMP_AFFINITY=scatter");
#pragma omp parallel for
for(x = 0; x<FLOPS_ARRAY_SIZE; x++)
{
sum += pow(log(cabs(A[x])),2);
}
printf("%10.31f\r\n",sum);
return( sum );
}


int main(int argc, char *argv[])
{
	//printf("Declaring srand\r\n");
	srand(time(NULL));
	//printf("Srand declared\r\n");
	int numthreads;
	double tstart, tstop, ttime;
	double gflops = 0.0;
	float a = 1.1;
	printf("Initializing\r\n");
	int x;

	FILE *myfile;
	myfile=fopen("space_delimited_data_stup.txt","r");
	double s,t,u,p;
	
	for(x=0;x<
	{
		printf("in the loop\r\n");
		//printf("this is new\r\n");
		if(x==0) numthreads = omp_get_num_threads();
		fscanf(myfile,"%lf",&s);
		//printf("line read\r\n");
		fscanf(myfile,"%lf",&t);
		fscanf(myfile,"%lf",&u);
		fscanf(myfile,"%lf",&p);
		//printf("declared s,t,u,and p\r\n");
		printf("s=%f t=%f u=%f p=%f\r\n",s,t,u,p);
		A[x] = igor_amplitude(s,t,u,p);
		//printf("ran the amplitdue function thing\r\n");
	}
	printf("Starting compute on %d threads\r\n",numthreads);
	
	tstart = dtime();
	lnl(A);
	tstop = dtime();
	gflops = (double)(1.0e-9*numthreads*LOOP_COUNT*MAXFLOPS_ITERS*FLOPSPERCALC);

	ttime = tstop-tstart;

	if((ttime)>0.0)
	{
	printf("GFlops = %10.31f, Secs = %10.31f, GFlops per sec = %10.31f\r\n", gflops, ttime, gflops/ttime);
	}
	return(0);
}
	
