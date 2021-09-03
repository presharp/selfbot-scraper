# written by imsofly#0001

import discum     

# put token here
user_token = ''

# OPTIONAL: CUSTOM TARGET SETTING (IF YOU LACK SPEAK PERMS OR WANT TO STEALTH)
# replace these with ids if you want to target custom channels (no message needed)
# otherwise make sure it is '' on both
target_guildid = ''
target_channelid = ''

# dont touch below
bot = discum.Client(token=user_token, log={"console":False, "file":False})
fetched = False

def close_after_fetching(resp, guild_id):
    global fetched
    try:
        print(str(len(bot.gateway.session.guild(guild_id).members)) + "..")
    except Exception:
        pass
    if bot.gateway.finishedMemberFetching(guild_id) and not fetched:
        fetched = True
        bot.gateway.removeCommand({'function': close_after_fetching, 'params': {'guild_id': guild_id }})
        members = bot.gateway.session.guild(guild_id).members
        
        f = open("scraped-" + guild_id + ".txt", "a")
        f.write(str(len(members)) + " members total\r\n"); 
        counter = 0
        for member in members:
            f.write(str(member) + "\n");
            counter += 1
            print(counter)
        f.close()
        
        lenmembersfetched = len(members) #this line is optional
        print(str(lenmembersfetched) + " members fetched")
        bot.gateway.close()

def get_members(guild_id, channel_id):
    global fetched
    fetched = False
    print("Starting scraping process for guild id " + guild_id +"...");
    f = open("scraped-" + guild_id + ".txt", "w")
    bot.gateway.fetchMembers(guild_id, channel_id, keep="all", wait=0.1) #get all user attributes, wait 1 second between requests
    bot.gateway.command({'function': close_after_fetching, 'params': {'guild_id': guild_id}})

@bot.gateway.command
def parse(resp):
    global fetched
    if resp.event.message:
        m = resp.parsed.auto()
        if m['content'] == '.avef':
            bot.deleteMessage(m['channel_id'], m['id']);
            get_members(m['guild_id'], m['channel_id']);

print("=========================================");
print("SELF-BOT SCRAPER! Written by... ImSoFly#0001");
if target_channelid != '' and target_guildid != '':
    print("Custom mode enabled.. Targeting guild id " + target_guildid + " at channel id " + target_channelid);
    get_members(target_guildid, target_channelid);
else:
    print("USAGE: Type .avef in any server channel of your choice. Check folder for files");
print("=========================================");
bot.gateway.run()

# written by imsofly#0001