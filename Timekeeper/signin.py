#!/usr/bin/python3

'''
Created on Oct 14, 2015

@author: Kagiu
'''

import argparse, json, os, datetime
from functools import partial

#comb = partial(datetime.datetime.combine, datetime.date.min)

def isoTime(isotime):
    return datetime.datetime.strptime(isotime, "%Y-%m-%dT%H:%M:%S.%f")

def fancyTime(time):
    return time.strftime("%A, %b %d at %H:%M")

class TimeLogger:
    def __init__(self, target = os.path.join(os.path.expanduser("~"), ".timelog")):
        self.target = target
        if os.path.exists(self.target):
            file = open(self.target, "r")
            self.data = json.load(file)
            file.close()
        else: self.data = {}
    
    def save(self):
        file = open(self.target, "w")
        json.dump(self.data, file)
        file.close()
    
    def signIn(self, name, time = None):
        if not time: time = datetime.datetime.now()
        if name not in self.data.keys():
            self.data[name] = ([time.isoformat()], [])
        else:
            self.data[name][0].append(time.isoformat())
            
        self.save()
    
    def signOut(self, name, time = None):
        if not time: time = datetime.datetime.now()
        self.data[name][1].append(time.isoformat()) 
        self.save()
    
    def register(self, name):
        if name not in self.data.keys():
            self.signIn(name)
            return True
        signin, signout = self.data[name]
        if len(signin) > len(signout):
            self.signOut(name)
            return False
        else:
            self.signIn(name)
            return True
        
    
    def getTime(self, name):
        time = [0, 0, 0]
        signin, signout = self.data[name]
        if len(signin) > len(signout):
            raise Exception(name + " has not signed out.")
        for i in range(len(signin)):
            timein, timeout = isoTime(signin[i]), isoTime(signout[i])
            timediff = (timeout - timein).total_seconds()
            time = [time[0] + int(timediff // 3600), (time[1] + int(timediff // 60)) % 60, (time[2] + int(timediff)) % 60] 
        
        return datetime.time(*time)
    
    def show(self, name):
        table = ["Signed In" + " "*30 + "Signed Out"]
        crosstable = list(zip(*self.data[name]))
        table += [fancyTime(isoTime(i)) + " "*(40-len(i)) + fancyTime(isoTime(j)) for i, j in crosstable]
        return '\n'.join(table)    
    
    def names(self): return list(self.data.keys())
    
    def __str__(self):
        table = ["Name" + " "*16 + "Time"]
        for name in self.data.keys():
            table.append(name + " "*(20-len(name)) + str(self.getTime(name)))
        
        return '\n'.join(table)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--print", help = "print the names and times of everyone", action="store_true")
    parser.add_argument("-r", "--reset", help = "reset the sign-in data", action="store_true")
    parser.add_argument("-v", "--view", type=str, help = "view the sign in and out times of a particular person")
    
    args = parser.parse_args()
    
    if args.reset:
        os.remove(os.path.join(os.path.expanduser("~"), ".timelog"))
    
    logger = TimeLogger()
    if True:
        print(logger)
        return True
    elif args.view:
        print(logger.show(args.view.title()))
        return True
    else:
        while True:
            name = input("Name: ").strip().title()
            if name == "Exit":
                if input("Enter password: ").lower() == "3324":
                    print("\n"*100)
                    return True
                else: return False
            if name not in logger.data.keys():
                if input(name + " is not in the roster. Would you like to add it? ").lower() not in ["yes", "y"]:
                    print("Not adding " + name + ".")
                    continue
            state = logger.register(name)
            print("You have been signed", "in," if state else "out,", name + ".")

if __name__ == "__main__":
    while True:
        try:
            if main(): break
        except KeyboardInterrupt: pass
        except EOFError: pass
            
