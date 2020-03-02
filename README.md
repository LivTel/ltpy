# ltrtml - Python module for sending observations to the Liverpool Telescope

## About
This module allows a pythonic way to;
* Submit observation groups to the Liverpool Telescope phase2 system
* Cancel and delete observation groups

### Features
* Supported instruments;
  * IO:O
  * IO:I
  * Sprat
  * FRODOSpec
* Single and multiple instrument groups (**apart from SPRAT**)
* Multiband observations with IO:O


## Dependencies
The module requires Python3 and has the following dependencies;
* suds-py3
* lxml

Both of these are listed in the requirements.txt and can be installed with;
```shell
pip install -r requirements.txt
```
## Usage

The structure of using ltrtml module is by creating 4 dictionary structures;
* `settings` -  holds RTML login, proposal and IP connection settings
* `target` - holds target name, RA and DEC.
* `constraints` - holds observing and timing constraints.
* `observation` - holds instrument settings and exposures.

The user can create any number of `observation` dictionaries to enable multi instrument groups or groups with multiple instrument setups.


**Please do not upload code containing `settings` dictionary to any public repository locations**


### Example Code

The example code in [example.py](example.py) gives example dictionary structures with commented options for settings and observations for each of the RTML enabled instrument on the telescope.

It also shows how to set up an LTObservation object, send and observation, check the list of `uids` and cancel an observation.


### Settings and connection
The module creates an LTObservation object that is initiated with a settings dictionary. The settings can be requested for any active proposal on the Liverpool Telescope by contacting ltsupprt_astronomer@ljmu.ac.uk.

The settings dictionary should be structured as follows and the object initiated by passing the settings;
```python
import ltrtml

settings = {
    'username': '',  # RTML_username
    'password': '',  # RTML_password
    'project': '',   # RTML_project name
    'LT_HOST': '',   # IP used to connect to the LT
    'LT_PORT': '',   # Port used to connect to the LT
    'DEBUG': False,  # Store all RTML responses for debugging, [True, False]
}


obs_object = ltrtml.LTObservation(settings)
```

#### Debug mode
Debug mode will save RTML requests and responses from the telescope to the local directory. This is used for diagnosing errors in the connection. To turn on set the dictionary element to `True`


### Creating `target`
```python
target = {
    'name': 'Vega',         # Target name, which will be first part of uid
    'RA': '18:36:56.336',    # Target ra 'HH:MM:SS.SS'
    'DEC': '+38:47:01.280',  # Target dec '+/-DD:MM:SS.SS'
}
```

### Creating `constraints`
```python
constraints = {
    'air_mass': '2.0',            # Maximum allowable Airmass Range 1 --> 3
    'sky_bright': '1.0',          # Maximum allowable Sky Brightness, Dark + X magnitudes
    'seeing': '1.2',              # Maximum allowable FWHM seeing
    'photometric': 'yes',         # Photometric conditions, ['yes', 'no']
    'start_date': '2020-02-18',   # Start Date 'YYYY-MM-DD'
    'start_time': '18:00:00.00',  # Start Time 'HH:MM:SS.SS'
    'end_date': '2020-02-280',    # End Date 'YYYY-MM-DD'
    'end_time': '00:00:00.00',    # End Time 'HH:MM:SS.SS'
}
```

### Creating `observations`

```python
observation = {
    'instrument': 'Sprat',
    'exp_time': '120.0',  # Image exposure time for target
    'exp_count': '3',     # Number of target images needed
    'grating': 'blue',    # Grating colour ['blue','red']
}
```

All elements in the dictionaries are strings and need to be formatted as shown above. Dictionary elements can be addressed and set directly, i.e.
```python
target['RA'] = '08:22:31.66'
observation['exp_time'] = '160'
```
### Sending observations
Once the observation dictionary is populated, the observation is sent to the telescope using the `submit_observation()` method.

```python
uid, error = obs_object.submit_observation(target, constraints, [observation1, observation2])
```

This returns a  `uid` (Unique IDentifier) string which is the observation `name` appended with the unix time of submission appended.

Also returned is an error string. The string is blank on success, but contains the error details if an error occurred.

### Getting list of obervation uids
The module stores the succesfully submitted observation uids in a pickled file.
This tuple of submitted observations can be obtained with;

```
uids = obs_object.getuids()
```


### Cancelling observations
Observations can be cancelled using the `uid` string returned when submitting an observation.

```python
error = obs_object.cancel_observation(uids)
```
Success returns a blank error string. If the cancel fails then the error string gives details of the failure.



## Support with using ltrtml
* For support or general questions, contact ltsupport_astronomer@ljmu.ac.uk
* For bugs or feature requests, raise these as issues in the github repository



## Authors

* **Kyle Medler** - *Implementation and Testing*
* **Doug Arnold** - *Guidance and Documentation*

## License
The code here is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
