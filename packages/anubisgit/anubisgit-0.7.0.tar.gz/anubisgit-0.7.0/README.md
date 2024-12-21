
![Anubis](https://images.unsplash.com/photo-1595853899417-4cc421f2998e?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2072&q=80)


# Anubis, a codemetrics tool.

You can read more about anubisgit on the [internal docummentation page page](http://open-source.pg.cerfacs.fr/anubisgit/).


##### Work in progress

Today, Anubis is essentially the script `timemachine.py`.
the time machine is a loop can spawn various versions  of a code from its gitbase, and perform analysis on it

##### Installation

Anubis I under fast development, and we do not update PiPY very often.
For a quick installation in a simplified virtual environment

```bash
python3 -m venv venv_anubisgit
source venv_anubisgit/bin/activate
python -m pip install 'anubisgit @ git+https://gitlab.com/cerfacs/anubisgit.git'
```

You can obiously install it from the sources available on [gitlab.com](https://gitlab.com/cerfacs/anubisgit)

##### main Usage

For now , there is a minimal CLI, limited to the execution of the time machine of Anubis
Type `>anubisgit` to see what is available :

```bash
 >anubisgit
Usage: anubisgit [OPTIONS] COMMAND [ARGS]...

  Package anubisgit v0.7.0

  ---------------    Anubis  --------------------

      You are now using the Command line interface of anubisgit package,     a
      set of tools created at CERFACS (https://cerfacs.fr).

      This is a python package currently installed in your python
      environement.

Options:
  --help  Show this message and exit.

Commands:
  anew          Create a default input file in current folder.
  authors-list  Retrieve authors list from joined_commits_monthly.json
  branches      Analyze branch health
  chronology    Code geology
  complexity    Analyse code health
  join-db       Join Anubis database
  timemachine   Build anubisgit database
```

If your new to anubisgit, you can find a quick how to tutorial [there](/docs/howto/howto_anubisgit.md)

##### Good practice

Althought anubisgit timemachine cli command won't let you start a run if your repository is not clean. It is highly recommended to git clone the repository you want to analyze and have a repository for your work repository to avoid any unwanted behaviour or file deletion during the timemachine process.


##### Most common troubleshoots

- Unclean repository
- .gitignore
  
##### Acknowledgements

![coec](https://www.hpccoe.eu/wp-content/uploads/elementor/thumbs/COEC_LOGO_RGB-01-pfvgeiplphmisuon437fk53iowou3j66yoeidghma6.png)

This work has been initially supported by the [COEC project](https://www.hpccoe.eu/coec/) which has received funding from the European Union’s Horizon 2020 research and innovation program under grant agreement No 952181 .
