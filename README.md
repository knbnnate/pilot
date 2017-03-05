# pilot
A repository for messing around with initial ideas for stuff

## RPG Character creation API and website

- [ ] Assign moderators on the back end - implement as PR approvers for the script/structure library?
- [x] Allow users to register
- [ ] Allow registered users to create a game instance and become DM
- [ ] Allow registered users to request access to a game instance from its DM
- [ ] Allow DM to accept users as members of a game instance
- [ ] Allow DM to hand off DM permissions to a game instance to another user
- [ ] Accept structured data and scripts defining character creation tables and rules

### Thoughts on data structure

Let's use a tiny subset of Shadowrun 5 character creation as an example here - thanks, [reddit](https://www.reddit.com/r/Shadowrun/comments/28b4q3/the_shadowrun_5_superbook/) and [shadowruntabletop.com](http://cdn.shadowruntabletop.com/wp-content/uploads/Downloads/CAT27000_Shadowrun%205_CharacterSheet.pdf?d131f9)

```
# Framework of what a character dictionary defaults to on initialization
character:
  player name: ""
  legal name: ""
  street name: ""
  major metatype: ""
  variant metatype: ""
  ethnicity: ""
  age: ""
  gender: ""
  sexuality: ""
  height: ""
  weight: ""
  street cred: 
  attributes:
    body:
      value: -1
      max: -1
    agility:
      value: -1
      max: -1
    reaction:
      value: -1
      max: -1
    strength:
      value: -1
      max: -1
    will:
      value: -1
      max: -1
    logic:
      value: -1
      max: -1
    intuition:
      value: -1
      max: -1
    charisma:
      value: -1
      max: -1
    edge:
      value: -1
      max: -1
  mutations:
    positive: []
    negative: []
  qualities:
    positive: []
    negative: []
  skill groups: []
  skills: []
  woke:
    magical: []
    technological: []


pools:
  abcde:
    - "A"
    - "B"
    - "C"
    - "D"
    - "E"

steps:
  - prioritize:
      pool: abcde
  - metatype

pools:
  metatype: 1
  attributes:
    a: 24
   
```

It has become clear I need to start off by focusing on the UI implementation with some minimal data that comes nowhere near the complexity of the Shadowrun rule set and character creation process.
