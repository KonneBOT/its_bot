# ITS_Bot  

Manager of the ITS Discord server.  

## Commands included:  


### /assign_roles

Automaticly assigns Roles, when a member chnages roles, based on the mapping in [``roles.py``](https://github.com/KonneBOT/its_bot/blob/main/roles.py), if a new course gets added to the server add the sign to the list [``courses``](https://github.com/KonneBOT/its_bot/blob/4fcea6afe1faac1ad660c704025322ef51843162/roles.py#L3C1-L3C45) in [``roles.py``](https://github.com/KonneBOT/its_bot/blob/main/roles.py) and run the command [``/create_roles``](#create_roles)

> run this command if the bot was down to assign all missed changes

### /assign_role_channel  

Takes in a *role* as arg and adds the *role* to the allowed roles to view this channel

### /create_roles 

Creates roles in the format of ``[1-7].Sem - [course]`` based on the courses given in [``roles.py.courses``](https://github.com/KonneBOT/its_bot/blob/4fcea6afe1faac1ad660c704025322ef51843162/roles.py#L3C1-L3C45)

### /delete_roles  

Deletes roles in the format of ``[1-7].Sem - [course]`` based on the courses given in [``roles.py.courses``](https://github.com/KonneBOT/its_bot/blob/4fcea6afe1faac1ad660c704025322ef51843162/roles.py#L3C1-L3C45) 

> in case something goes wrong

### /sort_roles  

Sorts all roles into one block to clean up the role overview

> [!NOTE]
>Currently not working for unkown reason

### /update_channels_pdf  
*(legacy: use [`update_channels_list`](#update_channels_list) instead)*  

Takes a *Modulhandbuch* pdf as arg and a *bool* whether or not the bot should create new channels or just eddit the matching existing ones and assign roles to them.

> [!CAUTION]
> Don't use it without knowing how the PDF should be formatted. That command was specifically designed for the *Modulhandbuch StuPO, 22.2* and **will not work** with others due to formatting changes.
>
> It can break and consequences are unknown (edit if someones actually trys it)  

### /update_channels_list 

Takes a *category* as arg and a *message.id* to create channels
First send a message with all the modul names.
For example: </br>
<sub> Wahlpflichtmodule WS2025/2026</sub>
```
Advanced Programming
Corporate Finance
Design Cyber Physical Systems
Embedded Programming
Entrepreneurship 
Hacking mit Python
Professionelle Java-Entwicklung: Software Engineering Instruments
Projektlösungen mit VBA (Visual Basic Applications)
Startup Finance
Sustainable Finance
Unternehmensplanspiel
```
the run the command ``/update_channels_list`` with the *message.id* of the message.</br>
The Bot will now give you the option to select the roles you want to add</br>
click submit and the bot will add the roles to the allready existing channels and create new channels with the roles for missing ones.

> [!NOTE]
> + you will need to click somewhere and resive the message ``✅ Stored {len(self.view.selected_ids)} role(s) so far.`` until you can change the page or to submit your choices
> + you can not remove roles ones they have been stored you can only cancel (yet)

> [!WARNING]
> The editing of existing channels has not been tested yet 

### easter_egg  

---

**YouTube:** [Adorable cat doing adorable things](https://www.youtube.com/watch?v=VZrDxD0Za9I&pp=ygUiYWRvcmFibGUgY2F0IGRvaW5nIGFkb3JhYmxlIHRoaW5ncw%3D%3D)  
