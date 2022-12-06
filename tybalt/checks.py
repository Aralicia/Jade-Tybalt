import os
from discord import Member, Role
from discord.ext import commands

def is_owner():
    async def predicate(ctx):
        return str(ctx.author.id) == os.environ.get('DISCORD_OWNER')
    return commands.check(predicate)

def user_can(permission, owner=None):
    if owner is not None:
        return is_owner() == owner
    async def predicate(ctx):
        return ctx.bot.permissions.match(ctx, permission)
    return commands.check(predicate)

class Rule:

    def __init__(self, guild, action, permission, sourceType, source, locationType, location, priority=None):
        self.guild = guild
        self.action = action
        self.permission = permission
        self.sourceType = sourceType
        self.source = source
        self.locationType = locationType
        self.location = location
        self.priority = priority
        if (self.priority is None):
            self.computePriority()

    def match(self, ctx):
        # check for guild
        if ctx.guild is None:
            return False
        elif ctx.guild.id != self.guild:
            return False

        #check for source
        if self.sourceType is not None:
            if self.sourceType == "role":
                return False
            elif self.sourceType == "user":
                return False
            else:
                return False

        #check for location
        if self.locationType is not None:
            if self.locationType == "channel":
                return False
            else:
                return False

        return True

    def computePriority(self):
        priority = 0
        if self.sourceType == "role":
            priority += 10
        elif self.sourceType == "group":
            priority += 11
        elif self.sourceType == "user":
            priority += 12
        if self.locationType == "channel":
            priority += 20
        self.priority = priority

class Permissions:

    def __init__(self, bot):
        self.bot = bot
        self.data = self.bot.data('Permissions')
        self.data.table('rules', {
            'id' : 'INTEGER PRIMARY KEY',
            'guild' : 'TEXT',
            'action' : 'TEXT',
            'permission' : 'TEXT',
            'sourceType' : 'TEXT',
            'source' : 'TEXT',
            'locationType' : 'TEXT',
            'location' : 'TEXT',
            'priority' : 'INTEGER'})

    def store(self, rule:Rule, commit=True):
        self.clear(rule, False)
        query = "INSERT INTO rules (guild, action, permission, sourceType, source, locationType, location, priority) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        params = (rule.guild, rule.action, rule.permission, rule.sourceType, rule.source, rule.locationType, rule.location, rule.priority)
        self.data.db.execute(query, params)
        if commit:
            self.data.db.commit()

    def clear(self, rule:Rule, commit=True):
        query = "DELETE FROM rules WHERE guild = ? and permission = ? and sourceType = ? and source = ? and locationType = ? and location = ?"
        params = (rule.guild, rule.permission, rule.sourceType, rule.source, rule.locationType, rule.location)
        self.data.db.execute(query, params)
        if commit:
            self.data.db.commit()

    def query(self, guild, permission):
        query = "SELECT guild, action, permission, sourceType, source, locationType, location, priority FROM rules WHERE guild = ? and permission = ? ORDER BY priority DESC"
        params = (guild.id, permission)
        res = self.data.db.execute(query, params).fetchall()
        return [Rule(*e) for e in res]

    def match(self, ctx, permission):
        currentPriority = None
        matches = []
        actions = set()
        for rule in self.query(ctx.guild, permission):
            if currentPriority is not None && rule.priority < currentPriority:
                break
            if rule.match(ctx):
                matches.append(rule)
                actions.add(rule.action)
                if currentPriority is None:
                    currentPriority = rule.priority

        if len(actions) == 0:
            return False #no rule. default to deny
        if len(actions) == 1:
            return actions.pop() == "allow"
        return False #conflicting rules with same priority match. default to deny

