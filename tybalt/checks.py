import os
from discord import Member, Role
from discord.ext import commands

def is_owner():
    async def predicate(ctx):
        return str(ctx.author.id) == os.environ.get('DISCORD_OWNER')
    return commands.check(predicate)

def has_prefix(prefix):
    async def predicate(ctx):
        return ctx.prefix == prefix
    return commands.check(predicate)

def user_can(permission, owner=True):
    async def predicate(ctx):
        if owner is not None:
            if str(ctx.author.id) == os.environ.get('DISCORD_OWNER'):
                return owner
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
        if str(ctx.guild.id) != self.guild:
            return False
        #check for source
        if self.check_source(ctx) == False:
            print("wrong source")
            return False
        #check for location
        if self.check_location(ctx) == False:
            print("wrong location")
            return False
        return True

    def describe(self, ctx):
        description = "{} {}".format(self.action, self.permission)
        if self.sourceType is not None:
            source = "###"
            if self.sourceType == "role":
                role = ctx.guild.get_role(int(self.source))
                if role is not None:
                    source = "@{}".format(role.name)
            elif self.sourceType == "group":
                source = self.source
            elif self.sourceType == "user":
                user = ctx.guild.get_member(int(self.source))
                if user is not None:
                    if user.nick is not None:
                        source = "@{} ({}#{})".format(user.nick, user.name, user.discriminator)
                    else:
                        source = "@{}#{}".format(user.name, user.discriminator)
            description = "{} for {}".format(description, source)
        if self.locationType is not None:
            location = "###"
            if self.locationType == "channel":
                channel = ctx.guild.get_channel(int(self.location))
                if channel is not None:
                    location = channel.mention
            description = "{} in {}".format(description, location)
        return description

    def computePriority(self):
        priority = 0
        if self.sourceType == "role":
            priority += 10
        elif self.sourceType == "group":
            priority += 11
        elif self.sourceType == "user":
            priority += 40
        if self.locationType == "channel":
            priority += 20
        self.priority = priority

    def check_source(self, ctx):
        if self.sourceType is None:
            return True
        if self.sourceType == "role" and self.user_has_role(ctx):
            return True
        if self.sourceType == "user" and str(ctx.author.id) == self.source:
            return True
        return False

    def check_location(self, ctx):
        if self.locationType is None:
            return True
        if self.locationType == "channel" and str(ctx.channel.id) == self.location:
            return True
        return False

    def user_has_role(self, ctx):
        for role in ctx.author.roles:
            if str(role.id) == self.source:
                return True
        return False

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
        if rule.sourceType is not None and rule.locationType is not None:
            query = "DELETE FROM rules WHERE guild = ? and permission = ? and sourceType = ? and source = ? and locationType = ? and location = ?"
            params = (rule.guild, rule.permission, rule.sourceType, rule.source, rule.locationType, rule.location)
        elif rule.sourceType is not None:
            query = "DELETE FROM rules WHERE guild = ? and permission = ? and sourceType = ? and source = ? and locationType IS NULL"
            params = (rule.guild, rule.permission, rule.sourceType, rule.source)
        elif rule.locationType is not None:
            query = "DELETE FROM rules WHERE guild = ? and permission = ? and sourceType IS NULL and locationType = ? and location = ?"
            params = (rule.guild, rule.permission, rule.locationType, rule.location)
        else:
            query = "DELETE FROM rules WHERE guild = ? and permission = ? and sourceType IS NULL and locationType IS NULL"
            params = (rule.guild, rule.permission)
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
            print(rule.describe(ctx))
            if currentPriority is not None and rule.priority < currentPriority:
                break
            if rule.match(ctx):
                print("Match!")
                matches.append(rule)
                actions.add(rule.action)
                if currentPriority is None:
                    currentPriority = rule.priority

        if len(actions) == 0:
            return False #no rule. default to deny
        if len(actions) == 1:
            return actions.pop() == "allow"
        return False #conflicting rules with same priority match. default to deny

