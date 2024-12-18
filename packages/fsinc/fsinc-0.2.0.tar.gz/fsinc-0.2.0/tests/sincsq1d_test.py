import numpy as np
import fsinc

def sincsq1d(x, s, xp):
  sp = np.zeros((xp.size,))

  for i in range(xp.size):
    for j in range(x.size):
      sp[i] += s[j] * np.sinc(x[j] - xp[i])**2

  return sp

def test_sincsq1d_2k(benchmark):
  x = np.linspace(-5, 5, 2000)
  s = np.sin(x)
  xp = np.linspace(-4.5, 4.4, 2000)

  benchmark(fsinc.sincsq1d, x, s, xp)

def test_sincsq1d_same():
  x = np.linspace(-5, 5, 100)
  s = np.random.uniform(-100, 100, x.size)

  sp = fsinc.sincsq1d(x, s, x, True)
  dp = sincsq1d(x, s, x)
  np.testing.assert_allclose(sp, dp, atol = 2e-3)

def test_sincsq1d_different_targets():
  x = np.linspace(-5, 5, 100)
  xp = np.linspace(-4, 3, 50)

  s = np.sin(x)

  sp = fsinc.sincsq1d(x, s, xp, True)
  dp = sincsq1d(x, s, xp)
  np.testing.assert_allclose(sp, dp, atol = 2e-3)

def test_sincsq1d_nu_to_u():
  x = np.random.uniform(-5, 5, 100)
  xp = np.linspace(-4, 3, 50)

  s = np.sin(x)

  sp = fsinc.sincsq1d(x, s, xp, True)
  dp = sincsq1d(x, s, xp)
  np.testing.assert_allclose(sp, dp, atol = 2e-3)

def test_sincsq1d_nu_to_nu():
  x = np.random.uniform(-5, 5, 100)
  xp = np.random.uniform(-4, 3, 50)

  s = np.sin(x)

  sp = fsinc.sincsq1d(x, s, xp, True)
  dp = sincsq1d(x, s, xp)
  np.testing.assert_allclose(sp, dp, atol = 2e-3)
