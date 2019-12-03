import sys
import os


header='''Group=SuperAdmin:changemap,cheat,private,balance,chat,kick,ban,config,cameraman,debug,pause,demos,featuretest,immunity,canseeadminchat,manageserver,private,reserve,forceteamchange
Group=Admin:chat,kick,pause,cheat,cameraman,reserve
Group=Moderator:reserve
Group=Whitelisted:reserve
Group=a:reserve
Group=Enforcer:changemap,chat,kick,canseeadminchat,reserve,forceteamchange,cameraman
Group=CamMan:reserve,cameraman
'''


'''
Basic user class to make handling the Whitelist data simpler
'''
class User:
    def __init__(self, steamid, name, permission='Whitelisted' ,group='UF'):
        self.steamid = steamid
        self.permission = permission
        self.name = name
        self.group = group


    # The str method prints the object in human readable format
    def __str__(self):
        return '{}:{}'.format(self.name,self.permission)


    def csv_line(self):
        return '{},{},{},{}'.format(self.name,self.group,self.permission,self.steamid)


    def whitelist_line(self):
        return 'Admin={}:{} // {}'.format(self.steamid,self.permission,self.name)



# This is surpurfluous, right now, don't code at 2 am. Keeping it in for handling user
# input, want to verify input, possibly check for duplicates
def add_user(steamid,name,permission='Whitelist',group='UF'):
    new_user = User(steamid,name,permission,group)
    print('Added user {} from group {} with permission {}'.format(name,group,permission))
    return new_user


def parse_entry(line,group):
    parsed=line.replace('Admin=','')
    parsed = parsed.replace('//',':')
    parsed = parsed.replace(' ','').rstrip()
    parsed = parsed.split(':')
    try:
        user = User(parsed[0],parsed[2],parsed[1],group)
    except IndexError:
        return None
    return user


def readlist(admins_file):
    with open(admins_file) as fin:
        for x in range(1,8):
            fin.readline()

        users = []
        group=''
        for line in fin:
            if not line:
                continue
            if "===" in line:
                group=fin.readline()
                group=group.lstrip().rstrip()
                continue
            elif line.isspace():
                continue
            user = parse_entry(line,group)
            if user is None:
                continue
            users.append(user)
 
        # This returns a list with only unique SteamIDs
        seen = set()
        uniq_users = [seen.add(u.steamid) or u for u in users if user.steamid not in seen]
               
        return uniq_users


def print_list(users, option=''):
    users.sort(key=lambda x:x.name.lower())
    users.sort(key=lambda x:x.group)

    groups = sorted(set(g.group for g in users))
    groups.remove('Super Admins')
    groups.insert(0,'Super Admins')
    
    if option == 'whitelist':
        print(header)   
    for g in groups:
        if not option == 'csv':
            print('\n'+'='*79)
            print(g+'\n')
        else:
            print('')
        for x in [y for y in users if y.group == g]:
            try:
                if option == 'whitelist':
                    print(x.whitelist_line())
                elif option == 'csv':
                    print(x.csv_line())
                else:
                    print(x)
            except:
                print('How the fuck did this break')


def main():
    users = readlist(sys.argv[1])
    if len(sys.argv) > 2:
        print_list(users,sys.argv[2])
    else:
        print_list(users)


if __name__ == '__main__':
    main()
