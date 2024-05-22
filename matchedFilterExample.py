# Plotting & Display
import matplotlib.pyplot as plt

# Configurations
import numpy as np
import scipy.signal as sp

sig = [1, 1, 0, 1, 1, 0, 0, 1] #test code
print(sig)
fig=plt.figure(figsize=(10,8))
plt.plot(sig, label='signal')
plt.xlabel('Sample')
plt.ylabel('Value')
plt.title('An Example Signal')
plt.grid()


sig_inzeros=np.hstack([np.zeros(4),sig,np.zeros(5)]) #test code in lager signal
plt.figure(figsize=(10,8))
plt.plot(sig_inzeros)
plt.xlabel('Sample')
plt.ylabel('Value')
plt.title('The Signal at Some Point in Time')
plt.grid()


signoise = np.random.rand(len(sig_inzeros))-0.5+sig_inzeros # add noise
plt.figure(figsize=(10,8))
plt.plot(signoise)
plt.xlabel('Sample')
plt.ylabel('Value')
plt.title('The Example Signal in Noise')
plt.grid()
plt.show()


#h = sig[::-1] # fliplr marched filter
#signoisemf = sp.lfilter(h, 1, signoise)
output = sp.correlate(signoise, sig) #convolving with matched filter is the same as corralating with ref signal 
plt.figure(figsize=(10,8))
plt.plot(output)
plt.xlabel('Sample')
plt.ylabel('Value')
plt.title('The Example Signal in Noise after Macthed Filtering')
plt.grid()
plt.show()









