data {
  int<lower=1> N;
  int<lower=1> K;
  matrix[N, K] X;
  vector[N] M1;
  vector[N] M2;
  vector[N] Y;
}

parameters {
  real a0_1;
  real a0_2;
  vector[K] a1;
  vector[K] a2;
  real b0;
  vector[K] cp;
  real b1;
  real b2;
  real<lower=0> sigma_m1;
  real<lower=0> sigma_m2;
  real<lower=0> sigma_y;
}

model {
  a0_1 ~ normal(0, 2);
  a0_2 ~ normal(0, 2);
  a1   ~ normal(0, 1);
  a2   ~ normal(0, 1);
  b0 ~ normal(0, 2);
  cp ~ normal(0, 1);
  b1 ~ normal(0, 1);
  b2 ~ normal(0, 1);
  sigma_m1 ~ exponential(1);
  sigma_m2 ~ exponential(1);
  sigma_y  ~ exponential(1);

  M1 ~ normal(a0_1 + X * a1, sigma_m1);
  M2 ~ normal(a0_2 + X * a2, sigma_m2);
  Y  ~ normal(b0 + X * cp + b1 * M1 + b2 * M2, sigma_y);
}

generated quantities {
  vector[K] ie1 = a1 * b1;
  vector[K] ie2 = a2 * b2;
  vector[K] total_ie = ie1 + ie2;
  vector[K] total_effect = cp + total_ie;
  vector[K] prop_mediated;
  for (k in 1:K) {
    prop_mediated[k] = total_effect[k] != 0 ? total_ie[k] / total_effect[k] : 0;
  }
}
