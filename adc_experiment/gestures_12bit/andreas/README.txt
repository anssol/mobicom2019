-----------------------------
Gestures
-----------------------------

* Push: A slower palm movement towards the sensor
* Pull: A slower palm movement away from the sensor

* Each gesture was performed at least 20 times per experiment, under the constraint of a 10 second time window.
* Later, we will perform the gestures under varying light levels, and with multiple users.

---------------------------
Samples information
---------------------------

* The samples are pure ADC values. 

* The samples can be normalized to (0,X) for now. Just plotting them will show the patterns.

---------------------------
Time information
---------------------------
Sample rate: 10.9 Hz

Total time (s) = (number of samples)/(sample rate)

----------------------------
Classification
----------------------------

I was thinking that the Pull and Pull can be differentiated by observing the relative time to 
reach the minimum from the start of a drop, and the time to rise back to 'normal' levels from the
minimum (e.g. by defining a threshold value).

-----------------------------
Other information
-----------------------------

* Measured light intensity for this experiment = 750 lx

* Two 'txt' files, can be opened as CSV using pandas library without any problem.

* The file 'andreas_pull_old' is the first experiment, and can be discarded.
