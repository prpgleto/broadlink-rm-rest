# dependencies - peewee, psycopg2-binary

from peewee import *
import json

# Local version
commands_db_path = 'commands.db'
# Docker version
# commands_db_path = '/data/commands.db'

commands_db = SqliteDatabase(commands_db_path)

## Commands DB classes and functions

class BaseCommandsModel(Model):
    class Meta:
        database = commands_db

class Target(BaseCommandsModel):
    uid = AutoField()
    name = TextField()

    def to_dict(self):
        return {"name": self.name}

    def get_command(self, name):
        return Command.get_or_none((Command.target == self) & (Command.name == name))
    
    def get_all_commands(self):
        return [command for command in self.commands]

    def get_all_commands_as_dict(self):
        return [command.to_dict() for command in self.commands]
    
    def add_command(self, name, value):
        
        if Command.get_or_none((Command.target == self) & (Command.name == name)):
            return False
        else:
            Command.create(target=self, name=name, value=value)
            return True
    
    def put_command(self, name, value):
        command = Command.get_or_none((Command.target == self) & (Command.name == name))
        
        if command:
            command.value = value
            command.save()
        else:
            Command.create(target=self, name=name, value=value)

    def update_command_name(self, old_name, new_name):
        command = Command.get_or_none((Command.target == self) & (Command.name == old_name)) 
        
        if command:
            command.name = new_name
            command.save()
            return True
        else:
            return False
    
    def delete_command(self, name):
        command = Command.get_or_none((Command.target == self) & (Command.name == name))
        
        if command:
            return bool(command.delete_instance())
        else:
            return False
    
    def update_name(self, new_name):
        self.name = new_name
        self.save()

class Command(BaseCommandsModel):
    uid = AutoField()
    target = ForeignKeyField(Target, backref="commands")
    name = TextField()
    value = TextField()

    def to_dict(self):
        return {"name": self.name, "value": self.value}

    def get_value(self):
        return value

def get_all_targets():
    try:
        targets = [target for target in Target.select()]
    except Target.DoesNotExist:
        targets = []

    return targets

def get_all_targets_as_dict():
    try:
        targets = [target.to_dict() for target in Target.select()]
    except Target.DoesNotExist:
        targets = []

    return targets

def get_target(name):
    return Target.get_or_none(Target.name == name)

def add_target(name):
    if Target.get_or_none(Target.name == name):
        return False
    else:
        Target.create(name=name)
        return True

def update_target_name(old_name, new_name):
    target = Target.get_or_none(Target.name == old_name)

    if target:
        target.name = new_name
        target.save()
        return True
    else:
        return False

def delete_target(name):
    target = Target.get_or_none(Target.name == name)

    if target:
        target.delete_instance(recursive=True, delete_nullable=True)
        return True
    else:
        return False