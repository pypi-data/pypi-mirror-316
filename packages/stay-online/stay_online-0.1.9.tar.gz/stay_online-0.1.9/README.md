# Simulate fake mouse movement and fake keyboard typing.

## How to use
### Start by running this command
```
from stay_online import stay_online
stay_online()
```
Once the Python program is initiated, a prompt will appear, requesting you to select the area where you want the cursor to move. 

This designated location will serve as the point where the cursor will autonomously navigate and perform left-click actions at specified intervals.
```
Place cursor at clicking position and left click once.
```
## Default optional values
```
stay_online(
        stop_hhmm:str='', 
        min_delay_seconds:int=120, 
        max_delay_seconds:int=180, 
        min_num_words:int=1, 
        max_num_words:int=10,
        show_timestamp:bool=False
        )
```
### Parameters
```
stop_hhmm: Automatically stop the simulation at the provided time, example '1700'.

min_delay_seconds: Minimum delay seconds between each new line.

max_delay_seconds: Maximum delay seconds between each new line.

min_num_words: Minimum number of words to type per line.

max_num_words: Maximum number of words to type per line.

show_timestamp: Type out the timestamp in front of the line to keep track of the time.
```