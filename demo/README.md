# Demo simulating three devices

This demo, simulates three devices which are two reservoirs and a valve which
connects between.

The reservoirs have three parameters: `temperature`, `humidity` and `volume`, while 
the valve has one parameter: `isActive`.

The simulation emulates the behavior when  liquid is flowing from one
reservoir to another while there are measurements of other variables.

The procedure is as follows:
1. Valve is OFF, reservoir1 is full, while reservoir2 is empty.
2. Valve is ON.
3. The reservoir1 is reducing its volume, while reservoir2 is increasing. Each
	 steps is about 100L.
4. The reservoir2 is full, while reservoir1 is empty.
5. Valve is OFF.
6. Wait for 2 measurements while valve is OFF.
7. Valve in ON.
8. The reservoir2 is reducing its volume, while reservoir1 is increasing. Each
	 steps is about 100L.
9. The reservoir1 is full, while reservoir2 is empty.
10. Restart the process as in 1.

The data taken in account for this demo is:

- Reservoir1:
	- DEVICE_TOKEN: `MY_TEST_DEVICE`
- Reservoir2:
	- DEVICE_TOKEN: `MY_TEST_DEVICE_2`
- Valve:
	- DEVICE_TOKEN: `MY_TEST_VALVE`
