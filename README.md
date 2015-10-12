Python bintray-publish-p2-updatesite
====================================

Python script which allows to manage a p2 update-site in Bintray. To run, clone this repository and execute the script, you must have python installed in your computer.  

**usage:**

publishToBintray.py [-h] [-m {upload,delete}] [-u U] [-k K] [-o O] [-r R] [-n N] [-e E] [-l L] [--version] {publish,discard}

This script can be used to manage an Eclipse p2 Updatesite in Bintray.

**positional arguments:**
```
  {publish,discard}   Publish all unpublished content for the given package
                      and version, including the last upload. If discard, any
                      unpublished content will be discarded and the
                      upload/delete arguments will be ignored.
```

**optional arguments:**
```
  -h, --help          show this help message and exit
  -m {upload,delete}  Whether the given files should be uploaded or deleted
                      from the repository.
  -u U                Bintray user
  -k K                Bintray API Key
  -o O                Repository owner, if other than user
  -r R                Repository name
  -n N                Package Name
  -e E                Package Version
  -l L                Path to repository location in local machine. If no
                      pathis given only the publish (POST) request is sent.
  --version           show program's version number and exit
```
