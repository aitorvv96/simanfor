# SIMANFOR

SIMANFOR, Support system for simulating Sustainable Forest Management Alternatives 

SIMANFOR is a tool to simulate different kind of operations over trees' plot. This tool is being develop by S|ngular using python and Apache Dask. 


### Prerequisites

Installing process. This tools includes some instalation script for each platform:

Windows Instalation

Linux and Mac Instalation

```
sudo install.sh
```

### Creating Scenario files


### How to use

Finally the simulator can be executed using the python program called main.py or using the run.sh script. For example if we can run a basic execution on **Linux** using a simple scenario file we should execute next line:

```
python3 main.py -s scenario.json
```

There are different options to execute this software:

```
usage: main.py [-h] -s scenario_file [-c configuration_file] [-e engine]
               [-logging_config_file logging_config_file] [-log_path log_path]
               [-v verbosity_level]
main.py: error: the following arguments are required: -s


```

Planning tool to run planners and domains using singularity containers. These are the different arguments:
```
-h, --help                show this help message and exit.
-s scenario_file     	  a path to the file with the information about 
			  the simulator and the scenario. 
-c configuration_file     a path to the file with the information about 
                          the main configuration of the simulator. The default 
			  configuration file is called simanfor.conf
-e engine                 a number parameter (integer) which defines 
			  the execution engine (1: Machine, 2: Cloud, 3: Super). 
			  The default value is 1 (Machine). 
-logging_config_file      a path to the file with the logging configuration.
-log_path path     	  a path to the location of the logging file. 
--v verbosity_level       a number parameter (integer) which defines the verbosity 
                          level of the simulator (1: Error, 5: Warning, 10 Warn, 15 Debug, 20 Info). 
			  The default value is 1 (Error).
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

