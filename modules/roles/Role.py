

class Role:
    def __init__(self, key, name, emoji, description):
        self.key = key
        self.name = name
        self.emoji = emoji
        self.description = description

    def role(self, guild):
        selfname = self.key.lower()
        roles = guild.roles
        for role in roles:
            if role.name.lower() == selfname:
                return role
        return None

    async def toggle(self, target, guild):
        role = self.role(guild)
        if role is None:
            raise ValueError("Role not Found in Guild")
        if role not in target.roles:
            await target.add_roles(role)
            return True
        else:
            await target.remove_roles(role)
            return False

