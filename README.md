# ltrtml - Python module for sending observations to the Liverpool Telescope

## About
This module allows a pythonic way to;
* Submit observation groups to the Liverpool Telescope phase2 system
* Cancel and delete observation groups

For more information on RTML and the Liverpool Telescope please see [https://telescope.livjm.ac.uk/PropInst/RTML/](https://telescope.livjm.ac.uk/PropInst/RTML/)

### Features
* Supported instruments;
  * IO:O
  * IO:I
  * Sprat
  * FRODOSpec
  * Moptop
* Multiple Targets and Observations in Group
* Single Instrument Groups only Supported at present
* Multiband observations with IO:O and Moptop


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
* `constraints` - holds observing and timing constraints.
* `target` - holds target name, RA and DEC. Multiple targets allowed
* `observation` - holds instrument settings, target and exposures. Multiple observations allowed.

The user can create any number of `observation` dictionaries to enable multi instrument groups or groups with multiple instrument setups.


**Please do not upload code containing `settings` dictionary to any public repository locations**


### Example Code

The example code in [example.py](example.py) gives example dictionary structures with commented options for settings and observations for each of the RTML enabled instrument on the telescope.

It also shows how to set up an LTObservation object, send an observation, check the list of `uids` (Unique IDentifiers) and cancel an observation.


### Settings and connection
The module creates an LTObservation object that is initiated with a settings dictionary. The settings can be requested for any active proposal on the Liverpool Telescope by contacting ltsupport_astronomer@ljmu.ac.uk.

The settings dictionary should be structured as follows and the object initiated by passing the settings;
```python
import ltrtml

settings = {
    'username': '',      # RTML_username
    'rtmlpass': '',      # RTML_password
    'proposal': '',      # RTML_proposal name
    'prefix': '',        # Prefix to Group UID
    'LT_HOST': '',       # IP used to connect to the LT
    'LT_PORT': '',       # Port used to connect to the LT
    'PKLFILE': 'pickle', # Name of picklefile for storing observations
    'DEBUG': False,      # Store all RTML responses for debugging, [True, False]
}


obs_object = ltrtml.LTObs(settings)
```

#### Debug mode
Debug mode will save RTML requests and responses from the telescope to the local directory. This is used for diagnosing errors in the connection. To turn on set the dictionary element to `True`


### Creating `target` dictionaries
More than one target can be observed within the group. This is useful for photometric or spectroscopic standards. These `target` dictionaries can have any name. RA AND DEC values **must** be strings formatted in the way shown. DEC **must** have a +/- sign prepending the value.

```python
target1 = {
    'name': 'Vega',         # Target name
    'RA': '18:36:56.336',    # Target ra 'HH:MM:SS.SS'
    'DEC': '+38:47:01.280',  # Target dec '+/-DD:MM:SS.SS'
}

target2 = {
    'name': 'Deneb',         # Target name
    'RA': '20:41:25.915',    # Target ra 'HH:MM:SS.SS'
    'DEC': '+45:16:49.220',  # Target dec '+/-DD:MM:SS.SS'
}

```

### Creating `constraints`
Contraints are appiled to all observations within the group. They are set up as below. All values in must be strings and formatted as shown below.

```python
constraints = {
    'air_mass': '2.0',            # Maximum allowable Airmass Range 1 --> 3
    'sky_bright': '1.0',          # Maximum allowable Sky Brightness, Dark + X magnitudes
    'seeing': '1.2',              # Maximum allowable FWHM seeing in arcsec
    'photometric': 'yes',         # Photometric conditions, ['yes', 'no']
    'start_date': '2020-02-18',   # Start Date 'YYYY-MM-DD'
    'start_time': '18:00:00.00',  # Start Time 'HH:MM:SS.SS'
    'end_date': '2020-02-280',    # End Date 'YYYY-MM-DD'
    'end_time': '00:00:00.00',    # End Time 'HH:MM:SS.SS'
}
```

### Creating `observations`
Observations specify one of the set up targets. They then specify the instrument and configuration, along with details of the exposure.

```python
observation = {
    'target': target1,
    'instrument': 'Sprat',
    'exp_time': '120',  # Integration time (s)
    'exp_count': '3',     # Number of Integrations
    'grating': 'blue',    # Grating colour ['blue','red']
}
```

**NOTE: All values in the dictionaries are strings** and need to be formatted as shown above.

Dictionary elements can be addressed and set directly, i.e.
```python
target1['RA'] = '08:22:31.66'
observation['exp_time'] = '160'
```
### Sending observations
Once the observation dictionary is populated, the observation is sent to the telescope using the `submit_observation()` method. 3 Arguments are passed, `target`, `constraints` and `observations`. The last argument is a tuple which can contain more than one observation. This is used for multiple target groups, or multiple observations with different instrument settings. For a single observation pass a single element tuple, e.g. `[observation]`.

```python
uid, error = obs_object.submit_group([observation1, observation2], constraints)
```

This returns a  `uid` (Unique IDentifier) string which is the `settings['prefix']` string with the unix time of submission appended. This `uid` will be the group name when viewed using the Phase2 UI tool.

Also returned is an error string. The string is blank on success, but contains the error details if an error has occurred.

### Getting list of obervation uids
The module stores the succesfully submitted observation uids in a pickled file.
This tuple of submitted observations can be obtained with;

```
uids = obs_object.getuids()
```


### Cancelling observations
Observations can be cancelled using the `uid` string returned when submitting an observation.

```python
error = obs_object.cancel_group(uids)
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
