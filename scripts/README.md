# Scripts

This is a set of boilerplate scripts describing the [normalized script pattern that GitHub uses in its projects](https://github.blog/2015-06-30-scripts-to-rule-them-all/). The [GitHub Scripts To Rule Them All
](https://github.com/github/scripts-to-rule-them-all) was used as a template. They were tested using MacOS Catalina version 10.15.5 and using GridOS 26, a derivative of Red Hat Fedora 26, on the Lincoln Laboratory Supercomputing Cluster.

- [Scripts](#scripts)
  - [Dependencies](#dependencies)
    - [Linux Shell](#linux-shell)
    - [Proxy and Internet Access](#proxy-and-internet-access)
    - [Superuser Access](#superuser-access)
  - [The Scripts](#the-scripts)
    - [script/setup](#scriptsetup)
  - [Distribution Statement](#distribution-statement)

## Dependencies

### Linux Shell

The scripts need to be run in a Linux shell. For Windows 10 users, you can use [Ubuntu on Windows](https://tutorials.ubuntu.com/tutorial/tutorial-ubuntu-on-windows#0). Specifically for Windows users, system drive and other connected drives are exposed in the `/mnt/` directory. For example, you can access the Windows C: drive via `cd /mnt/c`.

If you modify these scripts, please follow the [convention guide](https://github.com/Airspace-Encounter-Models/em-overview/blob/master/CONTRIBUTING.md#convention-guide) that specifies an end of line character of `LF (\n)`. If the end of line character is changed to `CRLF (\r)`, you will get an error like this:

```bash
./bootstrap.sh: line 2: $'\r': command not found
```

### Proxy and Internet Access

The scripts will download data using [`curl`](https://curl.haxx.se/docs/manpage.html) and [`wget`](https://manpages.ubuntu.com/manpages/trusty/man1/wget.1.html), which depending on your security policy may require a proxy.

The scripts assume that the `http_proxy` and `https_proxy` linux environments variables have been set.

```bash
export http_proxy=proxy.mycompany:port
export https_proxy=proxy.mycompany:port
```

You may also need to [configure git to use a proxy](https://stackoverflow.com/q/16067534). This information is stored in `.gitconfig`, for example:

```git
[http]
	proxy = http://proxy.mycompany:port
[https]
	proxy = http://proxy.mycompany:port
```

### Superuser Access

Depending on your security policy, you may need to run some scripts as a superuser or another user. These scripts have been tested using [`sudo`](https://manpages.ubuntu.com/manpages/disco/en/man8/sudo.8.html). Depending on how you set up the system variable, `AEM_DIR_CORE` you may need to call [sudo with the `-E` flag](https://stackoverflow.com/a/8633575/363829), preserve env.

If running without administrator or sudo access, try running these scripts using `bash`, such as

```bash
bash ./setup.sh
```

## The Scripts

Each of these scripts is responsible for a unit of work. This way they can be called from other scripts.

This not only cleans up a lot of duplicated effort, it means contributors can do the things they need to do, without having an extensive fundamental knowledge of how the project works. Lowering friction like this is key to faster and happier contributions.

The following is a list of scripts and their primary responsibilities.

### script/setup

[`script/setup`](setup.sh) is used to set up a project in an initial state. This is typically run after an initial clone, or, to reset the project back to its initial state. This is also useful for ensuring that your bootstrapping actually works well.

Note this script uses `wget` and `python` commands. Although this should be installed by the [`em-core`](https://github.com/Airspace-Encounter-Models/em-core)  initial setup, ensure that you have `wget` installed. If not, you can install `wget` on a Mac by via `brew install wget`. By activating the conda environment, this script should be able to execute the python commands.

## Distribution Statement

DISTRIBUTION STATEMENT A. Approved for public release. Distribution is unlimited.

© 2020 Massachusetts Institute of Technology.

This material is based upon work supported by the Federal Aviation Administration under Air Force Contract No. FA8702-15-D-0001.

Delivered to the U.S. Government with Unlimited Rights, as defined in DFARS Part 252.227-7013 or 7014 (Feb 2014). Notwithstanding any copyright notice, U.S. Government rights in this work are defined by DFARS 252.227-7013 or DFARS 252.227-7014 as detailed above. Use of this work other than as specifically authorized by the U.S. Government may violate any copyrights that exist in this work.

Any opinions, findings, conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the Federal Aviation Administration.

This document is derived from work done for the FAA (and possibly others), it is not the direct product of work done for the FAA. The information provided herein may include content supplied by third parties.  Although the data and information contained herein has been produced or processed from sources believed to be reliable, the Federal Aviation Administration makes no warranty, expressed or implied, regarding the accuracy, adequacy, completeness, legality, reliability or usefulness of any information, conclusions or recommendations provided herein. Distribution of the information contained herein does not constitute an endorsement or warranty of the data or information provided herein by the Federal Aviation Administration or the U.S. Department of Transportation.  Neither the Federal Aviation Administration nor the U.S. Department of Transportation shall be held liable for any improper or incorrect use of the information contained herein and assumes no responsibility for anyone’s use of the information. The Federal Aviation Administration and U.S. Department of Transportation shall not be liable for any claim for any loss, harm, or other damages arising from access to or use of data or information, including without limitation any direct, indirect, incidental, exemplary, special or consequential damages, even if advised of the possibility of such damages. The Federal Aviation Administration shall not be liable to anyone for any decision made or action taken, or not taken, in reliance on the information contained herein.
