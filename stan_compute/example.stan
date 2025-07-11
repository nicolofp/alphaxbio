data {
  int <lower=1> N;      // number of data points
  vector[N] wave;       // the wavelengths
  vector[N] flux;       // the observed flux values
}

parameters {
  real<lower=-1000, upper=1000> cont;  // continuum level
  real<lower=-100, upper=100> slope;   // continuum slope
  real<lower=0, upper=1000> amp;       // amplitude of Gaussian
  real <lower=0, upper=10> center;     // center of the line
  real <lower=0, upper=10> width;      // scale
}

model {
  vector[N] mod_flux;    // the model flux

  // continuum slope + Gaussian
  mod_flux = amp*exp(-0.5*square(center - wave)/square(width)) +
             cont + slope*wave;
  // Poisson is approximately Normal with sigma = sqrt(counts)
  flux ~ normal(mod_flux, sqrt(flux));
}
