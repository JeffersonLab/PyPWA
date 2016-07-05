#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
#include <complex.h>
#include <time.h>
#include <offload.h>
#define REAL double
complex double res;
int events;
double *S;
double *T;
double *U;
//readthedocs.org python wrapping c/c++ for python
__attribute__((target(mic)))void dummy_(double *ret);
__attribute__((target(mic)))void amp_(complex double *res, double *s, double *t, double *u, double *p);

__attribute__((target(mic))) void Initialize(double *s, double *t, double *u,int nEvents){
	S = s;
	T = t;
	U = u;
	events = nEvents;
	double blah = 1.0;
	#pragma offload target(mic)
	{
		dummy_(&blah);
	}
}

__attribute__((target(mic)))complex double igor_amplitude(complex double res, double s, double t, double u, double p){
	complex double ret;
	amp_(&ret,&s,&t,&u,&p);	
	return ret;
}

__attribute__((target(mic)))complex double* CalculateAmplitude(double p){
	omp_set_num_threads(120);
	double sum = 0.0;
	complex double *amplitudes = new complex double[events];
	#pragma offload target(mic) in(S[0:events],T[0:events],U[0:events]) inout(events,sum)
	{	
		complex double A;
		int x;
		#pragma omp parallel
		{
			#pragma omp for reduction(+:sum)
			for(x = 0; x<events; x++){
				amplitudes[x] = igor_amplitude(A,S[x],T[x],U[x],p);
			}	
		}
	}

	return amplitudes;	
}
