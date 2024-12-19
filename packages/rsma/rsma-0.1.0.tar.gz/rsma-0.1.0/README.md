# RSMA
Robotic State Management Architecture

# Description
This is a programming framework library used in robotics applications like Catbot and lil-strider bot for the Robotics Club of RIT.

# Problem Statement
In robotics applications, ongoing hardware development often leads to volatile low-level software, making it challenging to maintain stability and consistency which distracts us away from high-level software. The Robotic State Management Architecture framework addresses this issue by leveraging Python's modularity. It provides an automatic runtime build based on configuration files, ensuring that software can adapt seamlessly to hardware changes with a single configuration change. The framework aims to solve this problem while also introducing a modern pythonic syntax. This framework is utilized in projects such as Catbot and lil-strider bot for MDRC.

# How to convert from OOP to RSMA
lets say you have the following class:
```py
# some import statement

class RobotPart:
  leg: LegClass = None
  arm: ArmClass = None

  def __init__(self, leg, arm):
    self.leg = leg
    self.arm = arm

  def doLegThing(self, some_param) -> SomeReturnObject:
    return self.leg.doLegThings()
```

In OOP, code above is very typical, but here is the translated version of above in this framework

```py
# some import statement
import leg as leg_actions 
import arm as arm_actions

@device
@dataclass
class RobotPart:
  leg: LegClass = None
  arm: ArmClass = None

ctx = create_context("robotpart", (RobotPart,))

@parser(ctx)
def robotpart_parser(config_dict: dict) -> RobotPart:
  return RobotPart(**config_dict)

@device_action(ctx)
def doLegThing(dev: RobotPart, some_param) -> SomeReturnObject:
  return leg_actions.doLegThing(dev.leg)
```
This basically turns the module as a static class(by importing with the "as" keyword) and allow us to separate the state(RobotPart class) from the function(doLegThing function). The state will then be stored in ctx object which has a dictionary. The key of the dictionary can then be used to point to the specific device object that you want to do an action on like if "catbot" is the key to an instance of RobotPart class then we can call `doLegThing("catbot", some_param)`. The context will take the key and convert it to the state that it has in the dictionary and run the function. This helps us manage state in a central location and does not need to be managed in the main script.

# How is the key defined?
The key is called an identifier, and the identifier is defined in the single configuration file, ideally living in the root or src directory of the project or package. This framework uses JSON file as a default configuration format, but it does support any format as long as you can return an orderedDict. Here is an example config file in JSON format:
```json
{
  "arm": {
    "catbot_arm":{/** some parameter to initialize arm */},
  },
  "leg": {
    "catbot_leg":{/** some parameter to initialize leg */},
  },
  "robotpart": {
    "catbot": {"leg":"catbot_leg", "arm": "catbot_arm"},
    "strider": {"leg": {
      /** some parameter to initialize leg */
    }},
  }
}
```
The configuration file has one big dictionary where the key is the context name/identifier and the value is another dictionary where the key is the identifier of the device states in the context, and value is the parameters needed to initialize the state object.
The configuration file is read from top to bottom(because order matters and we use orderedDict), and if we need devices made in the lines above, we can reference their identifier string as used for "catbot".

# How do I run it?
Once everything above is defined, we can finally start writing the main script. The benefit of this framework is that it is very friendly on the run script because we do not have to manage instances, and we can just focus on calling functions that we need to call and point(with the identifier) to the device that we like to call the function on. This means if you have many sample scripts or test scripts, other than your main script, it is really easy to manage all of them at once. For example:
```py
import robot as robot_actions

CATBOT = "catbot"

def main():
  some_param = 0
  while True:
    robot_actions.doLegThing(CATBOT, some_param)
    some_param += 1

if __name__ == "__main__":
  main()
```
This is a totally valid syntax and as long as CATBOT does not change we can continue to run this, even if arm or leg is no longer the same arm configuration as before.

# Is this OOP?
Simple answer is "its python, so yes," but the more difficult answer is "you can think of it as OOP." Here is some things that this framework changes to OOP.
* Private Attribute: Every component's state is private by default. This is for security, but technically nothing is stopping you from making a function that just returns the state object which basically defeats the purpose of the context. If you are doing this: 1. how dare you and 2. you might as well uninstall this framework. A better solution might be a generic get method where you can just index the state and get its value.
* Inheritance: is now more restricted and only states can be inherited. There has been consideration to make actions inheritable, but that can be done with functions in the state class, but it is not recommended as you can not directly call them in the script file(this is a punishment for using too much OOP). You can argue with me on this all you want, but this kind of inheritance makes functions untrackable and hard to manage. This also goes against my next point.
* Reverse OOP's idea of functions live under states: while yes in certain ways this is true, it can just gets annoying. And its certainly not true for functions that just doesn't have states, and this is where most problems occur for OOP. This framework just lets you call functions at the level of a part that you want without having to go all the way down the robot's structure with the dot notation, and even better you don't even have to initialize the entire robot just to test out a small part of a robot.
* Modules as classes: this framework forces people to use modules as classes which makes files short and focus on one thing and one thing only. While nothing is technically stopping you from defining multiple contexts in a module, I recommend you don't for clarity and also give you options to import the only thing that is needed. I also believe this will help with rapid prototyping and incremental testing.

This framework was partly an exploration of the FP vs OOP conversation and while this framework uses both, I have realized that its more of a spectrum, and neither extreme is great. Thats where I landed on this middle ground where I liked some parts of OOP and FP but not all, but by utilizing both paradigms, I can control what parts of OOP and FP is acceptable. I am not going to defend either side of the argument, and I will also say that not all application can greatly benefit from this framework's mixture of FP and OOP, and I recommend exploring your comfortable mixture of OOP and FP for your use case. 

# Examples
Examples of this framework being used in real application can be found in the Catbot, and lil-strider repository below:
- [Catbot](https://github.com/RIT-MDRC/Catbot)
- [Strider](https://github.com/RIT-MDRC/lil-strider)