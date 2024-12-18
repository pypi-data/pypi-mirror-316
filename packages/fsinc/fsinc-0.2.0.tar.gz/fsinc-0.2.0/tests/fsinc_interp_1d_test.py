import numpy as np
import fsinc

import matplotlib.pyplot as plt

def test_1d_u_to_nu(plot):
  x = np.arange(0, 5, .001)
  # x = np.sort(np.random.uniform(0, 5, 5000))
  s = np.sin(2*np.pi*x) + 2 * np.cos(.2 * x)

  xp = np.sort(np.random.uniform(.2, 4.8, 2*x.size))
  print(x)
  print(xp)
  print(x.size, xp.size)
  sp = fsinc.sinc1d_interp_u(x, s, xp)

  ssp = np.sin(2*np.pi*xp) + 2 * np.cos(.2 * xp)

  if plot:
    plt.figure()
    plt.plot(x, s, label = 'uniform')
    plt.plot(xp, sp, '--', label = 'interp NU')
    plt.show()

  np.testing.assert_allclose(sp, ssp, rtol = 1.e-2, atol = 1e-3)

def test_1d_nu_to_u(plot):
  x = np.sort(np.random.uniform(-5, 5, 5000))
  s = np.sin(3*np.pi*x) + 2 * np.cos(.2 * x)
  # s = np.exp(-3*x**2)

  xp = np.arange(-4, 4, 1./100)
  print(x.size, xp.size)
  sp = fsinc.sinc1d_interp_nu2(x, s, xp, 20.)

  if plot:
    plt.figure()
    plt.plot(x, s, label = 'uniform')
    plt.plot(xp, sp, '--', label = 'interp NU')
    plt.show()

  ssp = np.sin(3*np.pi*xp) + 2 * np.cos(.2 * xp)
  np.testing.assert_allclose(sp, ssp, rtol = .01, atol = .05)


def test_1d_nu_to_nu2(plot):
  x = np.sort(np.random.uniform(-5, 5, 5000))
  s = np.sin(2*np.pi*x) + 2 * np.cos(.2 * x)

  xp = np.sort(np.random.uniform(-4, 4, 100))
  print(x.size, xp.size)
  sp = fsinc.sinc1d_interp_nu2(x, s, xp, 30.)

  if plot:
    plt.figure()
    plt.plot(x, s, label = 'uniform')
    plt.plot(xp, sp, '--', label = 'interp NU')
    plt.show()

  ssp = np.sin(2*np.pi*xp) + 2 * np.cos(.2 * xp)
  np.testing.assert_allclose(sp, ssp, rtol = .01, atol = .05)

def test_1d_nu_to_nu3(plot):
  x = np.sort(np.random.uniform(-5, 5, 5000))
  s = np.sin(2*np.pi*x) + 2 * np.cos(.2 * x)

  xp = np.sort(np.random.uniform(-4, 4, 100))
  print(x.size, xp.size)
  sp = fsinc.sinc1d_interp_nu3(x, s, xp, 30.)

  if plot:
    plt.figure()
    plt.plot(x, s, label = 'uniform')
    plt.plot(xp, sp, '--', label = 'interp NU')
    plt.show()

  ssp = np.sin(2*np.pi*xp) + 2 * np.cos(.2 * xp)
  np.testing.assert_allclose(sp, ssp, rtol = .01, atol = .39)

