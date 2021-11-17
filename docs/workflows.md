
# Gitflow Workflow

  

| Index |

| [Introduction](#introduction)|

| [Steps to follow](#steps-to-follow) |

| [Guidelines for Feature Branches](#guidelines-for-feature-branches)|

  

<a  name="introduction"></a>

## Introduction

  

We propose to adopt the **Gitflow Workflow** for collaborating on the software development. A clear description of the rationale of the workflow is reported at this [link](https://www.atlassian.com/git/tutorials/comparing-workflows#gitflow-workflow).

  

The main Gitflow guidelines, and their effects can be found below.

  

![Gitflow](https://github.com/Ho-lab-jaist/WoTT/blob/master/figures/Gitflow.png)

  

Two main branches are present: *master* and *develop*. The master branch stores the official release history, and the develop branch serves as the testbed for new features and functionalities.

*  **No one works on the master branch**

*  **No one works *directly* on the develop branch**

  

To work on new features, each developer must fork a _feature_ branch off of _develop_. Each new feature should reside in its own branch, which can be pushed to the shared “Software” repository for backup/collaboration. When a feature is complete, the developer merges the feature branch into develop and tests whether the newly added feature works properly or not.

  

Once *develop* has acquired enough features for a release and each developer has tested and documented the new features he has developed, admin forks a *release* branch off of develop. On the *release* branch no new features can be added (only bug and documentation fixes). All the developers test the whole software.

  

Once it's ready and working, admin merges *release* into *master* and tags it with a version number. In addition, admin merges *release* into *develop*.

  

To avoid conflicts, from the creation of the *release* branch up to its merging with *develop*, no *feature* branch should be merged into *develop*.

  
  

<a  name="steps-to-follow"></a>

## Steps to Follow

### Developing Phase

  

1. Clone the Software repository from the url

  

```

$ git clone {url}

```

2. Create locally a tracking branch for *develop*;

  

```

$ git checkout --track origin/develop

```

3. When starting to work on a new feature:


	 1. pull from _develop_ (this makes sure your local code is up to date.);

		```

		$ git pull

		```

	2. create a new branch _“feature/my-feature”_ from _develop_ (e.g. feature/new-action);

  

		```

		$ git checkout -b feature/my-feature

		```

4. Work on the created _my-feature_ branch in the usual way (edit, stage, commit, - optionally push to the remote repository, but feature branches can remain local -);

5. When the feature is ready (and the code is polished and commented):

	1. pull from _develop_ (this makes sure your local code is up to date. );

  

		```

		$ git checkout develop

		$ git pull

		```

	2. merge _my-feature_ branch into the _develop_ branch. Notice that the option --no-ff allows for generating a merge commit (even if it is a fast-forward merge) providing a useful way to document all merges that occurred in the repository. Please use it;

  

		```

		$ git merge --no-ff feature/my-feature

		```

	3. test your new features with the updated code ;

	4. push to _develop_ (only when testing is successful);

  

		```

		$ git push

		```

6. Repeat steps from 3 to 5.4 for each new feature.

  

Please give meaningful names to *feature* branches. The use of slashes in branches’ names allows for grouping branches.

  

All the previous steps can be executed through the command line or any git desktop client. We suggest the use of GitKraken cross-platform desktop client (https://www.gitkraken.com/) since it provides a very easy to use and convenient interface for working with the Gitflow Workflow (https://support.gitkraken.com/repositories/git-flow).

### Releasing Phase

  

Admin is in charge to handle the *release* and the *master* branches.

  
  
  
  

<a  name="guidelines-for-feature-branches"></a>

## Guidelines for Feature Branches

  

The guidelines for pushing a _feature_ branch to the remote are:
  

* No push, only merge (with the merge commit option): if it is a short and simple feature carried out by one person only (of course, after the merge, you have to push to _develop_). E.g. adding an action to the action library, small changes to the code…

* Push and merge (with the merge commit option): if it is a long and important feature, if more people must collaborate on it, if it is a feature which other developers are expected to test on the feature branch. E.g. the choice manager is currently on an open feature branch on the remote, it will be merged only after developers have installed naoqi with root permissions and tested it.

  

The above rules for pushing a feature branch are not strict, the rationale is that incomplete, experimental or not working features are NOT merged into the _develop_ branch and that the repository is always kept as an effective shared/collaborative folder rather than a collection of personal backups.
