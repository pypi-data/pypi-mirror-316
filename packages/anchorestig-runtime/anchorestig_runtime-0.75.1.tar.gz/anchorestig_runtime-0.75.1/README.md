# Anchore Runtime STIG

Anchore STIG is a complete STIG solution that can be used to run STIG profile against running containers in a cluster.

## Description

Use Anchore STIG to perform STIG checks against running containers in Kubernetes environments or static Docker images from a registry or stored locally. The tool executes automated scans against specific STIG Security Guide (SSG) policies. The program will output either a JSON report with a summary of STIG check results for runtime checks or XCCDF XML and OpenSCAP XML and HTML for static checks. 

The runtime functionality includes the following profiles:

* Ubuntu 20.04 (ubuntu-20.04)
* Ubuntu 22.04 (ubuntu-22.04)
* Universal Base Image 8 (ubi8) - This runs the full RHEL 8 STIG
* Universal Base Image 9 (ubi9) - This runs the full RHEL 9 STIG
* Postgres 9 (postgres9)
* Apache Tommcat 9 (apache-tomcat9)
* Crunchy PostgreSQL (crunchy-postgresql)
* JBOSS (jboss)
* Java Runtime Environment 7 (jre7)
* MongoDB Enterprise (mongodb)
* nginx (nginx)

## Getting Started

### Dependencies

#### Overall
* `python3 >= 3.8 with pip3 installed`
* `make`

#### Runtime
* `kubectl exec` privileges
* Pods running one of the above listed software / OS types

### Install

* clone the repo
* run `make` to install 

### Running the Program

#### Runtime

* Run `anchorestig runtime` from the terminal. 
    * NOTE: This edition of the demo has been optimized for single-container pods by default

* The program will run in interactive mode by just executing `anchorestig runtime --interactive` from the terminal, however, you may also use the following CLI input parameters:

```
CLI Input Parameters:

  -i, --image TEXT       Specify profile to use. Available options are
                         ubuntu-20.04, ubuntu-22.04, ubi8, ubi9, postgres9,
                         apache-tomcat9, crunchy-postgresql, jboss, jre7,
                         mongodb, nginx
  -p, --pod TEXT         Any running pod running an image that runs one of the
                         specififed profile's software
  -c, --container TEXT   Container in the pod to run against
  -o, --outfile TEXT     Output file name. Only JSON output filetype is
                         supported (include the '.json' extension with the
                         output file name in CLI)
  -n, --namespace TEXT   Namespace the pod is located in
  -u, --usecontext TEXT  Specify the kubernetes context to use
  -b, --aws-bucket TEXT  Specify the S3 bucket to upload results to. Omit to
                         skip upload
  -a, --account TEXT     Specify the Anchore STIG UI account to associate the
                         S3 upload with. Omit to skip upload
  -t, --interactive      Run in interactive mode
  -s, --sync             Sync policies from Anchore
  --help                 Show this message and exit.

```
Ex: `anchorestig-runtime runtime -u current -n test -i postgres9 -p postgres9 -c default -o postgres.json`

* NOTE: The output file will be saved to the `./outputs` directory

##### Viewing Results

Navigate to the `./outputs` directory to view the output file. 

## Help

Use the `--help` flag to see more information on how to run the program:

`anchorestig-runtime runtime --help`

## CINC Functionality Explanation

`cinc-auditor` allows users to specify a target to run profiles against. This can be a number of things including SSH targets or a local system. The `train-k8s-container` plugin allows our STIG tool to target a kubernetes namespace, pod, and container to run cinc profiles against. When a container is set as the target, each individual control will be prepended with `kubectl exec .....` and the appropriate commands to run within the container and retireve the results to make the determination of a pass or fail against the control baseline.

## Modifying Controls

The `policies` directory contains sub-directories for the Ubuntu, UBI, and Postgres STIG profiles. Each directory has a `tar.gz` file that can be decompressed. From there, each control that runs is defined as a ruby gem file in the `controls` directory. The ID of each control (displayed in Heimdall) is pulled from the `control` section at the beginning of the ruby gem file. To change what is displayed, change the control id at the beginning of the file.

## Adding Not-Applicable Controls

The `UBI 8` and `Ubuntu 20.04` policies were built with the `not-applicable` rules removed. To add them back, untar the tar files in each repository, move the ruby gem files from the `not-applicable/` directory to the controls directory. Then run `cinc-auditor archive .` in the untarred directory. This will generate a new tar archive file. Replace the original archive, that you un-tarred at the beginning with the newly generated one and the newly included rules will run.

## Authors

* Sean Fazenbaker 
[@bakenfazer](https://github.com/bakenfazer)
* Michael Simmons 
[@MSimmons7](https://github.com/MSimmons7)

<!-- ## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the Anchore License - see the LICENSE.md file for details -->