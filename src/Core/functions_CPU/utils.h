/*
Copyright 2019 Daniil Kazantsev

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#include <stdlib.h>
#include <memory.h>
#include "omp.h"
#ifdef __cplusplus
extern "C" {
#endif
float copyIm(float *A, float *U, long dimX, long dimY, long dimZ);
unsigned char copyIm_unchar(unsigned char *A, unsigned char *U, int dimX, int dimY, int dimZ);
float copyIm_roll(float *A, float *U, int dimX, int dimY, int roll_value, int switcher);
#ifdef __cplusplus
}
#endif
