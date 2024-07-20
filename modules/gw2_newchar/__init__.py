import discord
from random import choice, randrange
from tybalt import checks
from discord.ext import commands
from discord import Message, MessageType

async def setup(bot):
    await bot.add_cog(TybaltNewchar(bot))

async def teardown(bot):
    await bot.remove_cog('TybaltNewchar')


class TybaltNewchar(commands.Cog):
    """Tybalt Newchar."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    @checks.user_can('newchar')
    async def newchar(self, ctx):
        # Chargen
        char = {}
        self.random_race(char)
        self.random_gender(char)
        self.random_profession(char)
        self.random_personality(char)
        self.random_name(char, ctx.message.author.display_name)

        # Generate Embed
        title = ""
        description = ""
        colour = self.get_colour(char)

        embed = discord.Embed(title=title, description=description, colour=colour)
        embed.set_thumbnail(url=self.get_thumbnail(char))
        embed.set_author(name=char['name'], icon_url=self.get_icon(char))
        embed.add_field(name="Profession", value=char['profession'])
        embed.add_field(name="Race & Gender", value="{} {}".format(char['gender'], char['race']))
        embed.add_field(name="Biography - {}".format(char['bio_profession'][0]), value="{} {}".format(char['bio_profession'][1], char['bio_profession'][2]), inline=False)
        embed.add_field(name="Biography - Personality", value="{} {}".format(char['bio_personality'][0], char['bio_personality'][1]), inline=False)
        embed.add_field(name="Biography - {}".format(char['bio_race_1'][0]), value="{} {}".format(char['bio_race_1'][1], char['bio_race_1'][2]), inline=False)
        embed.add_field(name="Biography - {}".format(char['bio_race_2'][0]), value="{} {}".format(char['bio_race_2'][1], char['bio_race_2'][2]), inline=False)
        embed.add_field(name="Biography - {}".format(char['bio_race_3'][0]), value="{} {}".format(char['bio_race_3'][1], char['bio_race_3'][2]), inline=False)

        response = choice([
            "I think you will like this one.",
            "Have you tried this ?",
            "A great character for a great person.",
            "How about that ?",
            "Here's what I thought for you.",
            "Maybe this one ? Not sure. You're a bit hard to grasp.",
        ])

        await ctx.send(response, embed=embed, reference=ctx.message)


    def random_race(self, char):
        char['race'] = choice(["Asura", "Charr", "Human", "Norn", "Sylvari"])
        match char['race']:
            case "Asura" :
                char['bio_race_1'] = ("College", "I'm a member of the College of", choice(["**Statics**", "**Dynamics**", "**Synergetics**"]))
                char['bio_race_2'] = ("Creation", "My first creation was", choice(["the **VAL-A golem**", "a **Transatmospheric Converter**", "an **Infinity Ball**"]))
                char['bio_race_3'] = ("Advisor", "My first advicsor was", choice(["**Bronk**", "**Zinga**", "**Blipp**", "**Canni**"]))

            case "Charr" :
                char['bio_race_1'] = ("Legion", "I am proud to be", choice(["a **Blood Legion** soldier", "an **Ash Legion** soldier", "an **Iron Legion** soldier"]))
                char['bio_race_2'] = ("Partner", "My sparring is", choice(["**Maverick** the soldier", "**Euryale** the elementalist", "**Clawspur** the thief", "**Dinky** the guardian", "**Reeva** the engineer"]))
                char['bio_race_3'] = ("Father", "My father is", choice(["a **Loyal Soldier**", "a **Sorcerous Shaman**", "a **Honorless Gladium**"]))

            case "Human" :
                char['bio_race_1'] = ("Upbringing", "I grew up", choice(["as a **Street Rat**", "as a **Commoner**", "among the **Nobility**"]))
                char['bio_race_2'] = ("Regret", "My biggest regret is", choice(["my **Unknown Parents**", "my **Dead Sister**", "a **Missed Opportunity**"]))
                char['bio_race_3'] = ("Blessing", "I was blessed by", choice(["**Dwayna**", "**Grenth**", "**Balthazar**", "**Melandru**", "**Lyssa**", "**Kormir**"]))

            case "Norn" :
                char['bio_race_1'] = ("Quality", "My most important quality is the", choice(["**Strength** to defeat acient foes", "**Cunning** to protect the spirits", "**Intuition** to guard the Mists"]))
                char['bio_race_2'] = ("Shameful Event", "In a recent Moot, I", choice(["**blacked out**", "**got in a fight**", "**lost an heirloom**"]))
                char['bio_race_3'] = ("Guardian Spirit", "My Guardian Spirit is", choice(["**Bear**", "**Snow Leopard**", "**Wolf**", "**Raven**"]))

            case "Sylvari" :
                char['bio_race_1'] = ("Vision", "I had a vision of the", choice(["**White Stag**", "**Green Knight**", "**Shield of the Moon**"]))
                char['bio_race_2'] = ("Ventari's Teaching", "The most important of Ventari's teaching is", choice(["**Act with wisdom, but act.**", "**All things have a right to grow.**", "**Where life goes, so too, should you.**"]))
                char['bio_race_3'] = ("Cycle", "The Pale Tree awakened me during", choice(["the **Cycle of Dawn**", "the **Cycle of Noon**", "the **Cycle of Dusk**", "the **Cycle of Night**"]))


    def random_gender(self, char):
        char['gender'] = choice(["Male", "Female"])

    def random_profession(self, char):
        char['profession'] = choice(["Elementalist", "Engineer", "Guardian", "Mesmer", "Necromancer", "Ranger", "Revenant", "Thief", "Warrior"])
        match char['profession']:
            case "Elementalist":
                char['bio_profession'] = ("Gem", "I wear a gem of", choice(["**Water**", "**Fire**", "**Earth**", "**Air**"]))
            case "Engineer":
                char['bio_profession'] = ("Tool", "My tool is", choice(["a **Universal Multitool Pack**", "**Eagle-Eye Goggles**", "a **Panscopic Monocle**"]))
            case "Guardian":
                char['bio_profession'] = ("Armor", "I wear", choice(["**Conqueror's Pauldrons**", "**Fanatic's Pauldron**", "a **Visionary's Helm**"]))
            case "Mesmer":
                char['bio_profession'] = ("Mask", "My mask is", choice(["**Harlequin's Smile**", "**Phantasm of Sorrow**", "**Fanged Dread**"]))
            case "Necromancer":
                char['bio_profession'] = ("Tatoo", "I mark my face with the symbol of a", choice(["**Trickster Demon**", "**Skull**", "**Ghostly Wraith**"]))
            case "Ranger":
                match char['race']:
                    case "Asura":
                        char['bio_profession'] = ("Pet", "My pet is a", choice(["**Moa**", "**Stalker**", "**Drake**"]))
                    case "Charr":
                        char['bio_profession'] = ("Pet", "My pet is a", choice(["**Devourer**", "**Stalker**", "**Drake**"]))
                    case "Human":
                        char['bio_profession'] = ("Pet", "My pet is a", choice(["**Bear**", "**Stalker**", "**Drake**"]))
                    case "Norn":
                        char['bio_profession'] = ("Pet", "My pet is a", choice(["**Bear**", "**Wolf**", "**Snow Leopard**"]))
                    case "Sylvari":
                        char['bio_profession'] = ("Pet", "My pet is a", choice(["**Moa**", "**Stalker**", "**Fern Hound**"]))
            case "Revenant":
                char['bio_profession'] = ("Blindfold", "I fight with my", choice(["**Mist Scrim** blindfold", "**Veil Piercer** blindfold", "**Resplendent Curtain** blindfold"]))
            case "Thief":
                char['bio_profession'] = ("Mask", "I understand the power of", choice(["**Anonymity**", "**Determination**", "**Subterfuge**"]))
            case "Warrior":
                char['bio_profession'] = ("Helm", "I wear", choice(["a **Spangenhelm**", "a **Galea**", "no helm at all"]))

    def random_personality(self, char):
        char['bio_personality'] = ("I use my", choice(["**Charm** to overcome trouble", "**Dignity** to overcome trouble", "**Ferocity** to overcome trouble"]))

    def random_name(self, char, basename):
        prefixes = ["Agent","Apprentice","Archivist","Explorer","Scholar","Researcher"];
        suffixes = [];

        #match char['profession']:
        #    case "Elementalist":
        #        prefixes.extend(['Arcanist'])
        #    case "Engineer":
        #        prefixes.extend(['Engineer'])
        #    case "Mesmer":
        #        prefixes.extend(['Arcanist'])
        #    case "Necromancer":
        #        prefixes.extend(['Arcanist'])

        match char['race']:
            case "Asura":
                college = char['bio_race_1'][1].strip('*')
                prefixes.extend(['Assistant','Golemancer','Technician', '{} Apprentice'.format(college),'{} Expert'.format(college), '{} Researcher'.format(college), 'Krewe Apprentice', 'Krewe Assistant', 'Krewe Leader', 'Krewe Member', 'Lab Apprentice','Lab Assistant','Lab Chief','Lab Worker','Peacemaker','Professor'])
            case "Charr":
                prefixes.extend(['Centurion','Gladium','Legionnaire','Sentinel'])
            case "Human":
                prefixes.extend(['Baron','Baroness','Captain','Exemplar','Deputy', 'Lord', 'Lady', 'Priest', 'Priestess','Vanguard'])
            case "Norn":
                spirit = char['bio_race_3'][1].strip('*')
                prefixes.extend(["{} Adept".format(spirit), "{} Shaman".format(spirit), 'Hunter', 'Shaman', 'Skaald'])
            case "Sylvari":
                prefixes.extend(['Gardener','Valiant','Warden','Mender'])
        
        name = basename
        if randrange(1, 5) > 1 :
            name = "{} {}".format(choice(prefixes), name)
        char['name'] = name

    def get_colour(self, char):
        match char['profession']:
            case "Elementalist":
                return 0xF68A87
            case "Engineer":
                return 0xD09C59
            case "Guardian":
                return 0x72C1D9
            case "Mesmer":
                return 0xB679D5
            case "Necromancer":
                return 0x52A76F
            case "Ranger":
                return 0x8CDC82
            case "Revenant":
                return 0xD16E5A
            case "Thief":
                return 0xC08F95
            case "Warrior":
                return 0xFFD166
        return 0xBBBBBB

    def get_thumbnail(self, char):
        match char['profession']:
            case "Elementalist":
                return "https://wiki.guildwars2.com/images/a/a2/Elementalist_icon.png"
            case "Engineer":
                return "https://wiki.guildwars2.com/images/4/41/Engineer_icon.png"
            case "Guardian":
                return "https://wiki.guildwars2.com/images/c/cc/Guardian_icon.png"
            case "Mesmer":
                return "https://wiki.guildwars2.com/images/3/3a/Mesmer_icon.png"
            case "Necromancer":
                return "https://wiki.guildwars2.com/images/6/62/Necromancer_icon.png"
            case "Ranger":
                return "https://wiki.guildwars2.com/images/9/9c/Ranger_icon.png"
            case "Revenant":
                return "https://wiki.guildwars2.com/images/8/89/Revenant_icon.png"
            case "Thief":
                return "https://wiki.guildwars2.com/images/d/d8/Thief_icon.png"
            case "Warrior":
                return "https://wiki.guildwars2.com/images/c/c8/Warrior_icon.png"
        return None

    def get_icon(self, char):
        match char['race']:
            case "Asura":
                return "https://wiki.guildwars2.com/images/1/1f/Asura_tango_icon_20px.png"
            case "Charr":
                return "https://wiki.guildwars2.com/images/f/fa/Charr_tango_icon_20px.png"
            case "Human":
                return "https://wiki.guildwars2.com/images/e/e1/Human_tango_icon_20px.png"
            case "Norn":
                return "https://wiki.guildwars2.com/images/3/3d/Norn_tango_icon_20px.png"
            case "Sylvari":
                return "https://wiki.guildwars2.com/images/2/29/Sylvari_tango_icon_20px.png"
        return None

