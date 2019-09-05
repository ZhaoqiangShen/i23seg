/*
Copyright 2019 Daniil Kazantsev & Diamond Light Source ltd.

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

#include <math.h>
#include <stdlib.h>
#include <memory.h>
#include <stdio.h>
#include "omp.h"
#include "utils.h"

/*
 * Output:
 */

#ifdef __cplusplus
extern "C" {
#endif
float chan_vese_main(float *Input, float *mask, float *Phi_x, float *Phi_xy, float *Phi_xx, float *Phi_y, float *Phi_yx, float *Phi_yy, float dt, float eta, float epsilon, float alpha_in, float alpha_out, int iterationsNumb, int dimX, int dimY, int dimZ);
#ifdef __cplusplus
}
#endif