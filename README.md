# Command Reservoir (cmdr)
A lot of power users always use shell commands and eventually forgot them. What happen when you forgot them? You clutter mycmd.txt, importantcommands.txt, donforgetthis.bat on your desktop. __cmdr__ is an easy and simple solution made to solve that problem. Every commands will be made accessible from the command line and all of the commands are stored in a simple and readable yaml file. __cmdr__ will allow all of the commands to be searched, executed, and copied to the clipboard!

## Get Started
Download __[cmdr.exe](https://github.com/downloads/ceilfors/command-reservoir/cmdr.exe)__ and include it to your PATH variable.

Open up your command prompt and type `cmdr -h`. Notice that a new file named cmdr.yaml will be created in the same path of your cmdr.exe. This will be the file that is treated as a storage. You can either add your commands here directly or from the command line interface.

Each __*action*__ in cmdr has these attributes:

1. A *name* that will be the unique identifer of the action.
1. *description* of the action that is optional. Supports tagging.
1. List of commands and command's answers. This list are called *statements* in the action's attribute.
  - *command* will be executed when the action is called
  - *answer* will provide the input stream to the executed command when needed

See the following example that will describe the action's attributes; this would be the format of an action in the cmdr.yaml if you are to manually write it there too:

    question: # action's name
    - description: Answers the question automatically with +cmdr  #action tagged with 'cmdr'
    - statement:  
      - python question.py         # first command
      - < first name               # first answer to the first command
      - < first age                # second answer to the first command
      - python question.py         # second command
      - < second name              # first answer to the second command
      - < second age               # second answer to the second command

When this action is available in your storage, it would be able to be executed with `cmdr exe question` in your command line. What would be the output? Say the question.py content is as simple as this:

    name = raw_input("Name: ")
    age = raw_input("Age: ")
    print "Name entered:", name
    print "Age entered:", age
    
When the action is executed, the output will be

    Name: Age: Name entered: first name
    Age entered: first age
    Name: Age: Name entered: second name
    Age entered: second age

## Interface  
* `get <name>`: print the detail of the specified action
* `add`: start an interactive prompt to add a new action
* `del <name>`: delete the specified action
* `all`: print all of action available
* `find <keyword> [-d] [-s]`: search for actions matched with keyword. Will search in description when -d is enabled and in statements when -s is enabled
* `exe <name>`: execute an action
* `copy <name> [-v]`: copy an action's command to to the clipboard. Copies the whole detail of the command when -v is enabled

## Futures
* Supporting string template in the command

## Caveats
* When the command to be executed is a `java` command. System.console() won't be available, which means NPE will be thrown.
* cmdr won't know how many answers (inputs) does the command need.
