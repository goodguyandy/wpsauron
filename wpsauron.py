from src.checks import *
import argparse
from src.project import Project
import validators

banner = """
               Three::rings
          for:::the::Elven-Kings
       under:the:sky,:Seven:for:the
     Dwarf-Lords::in::their::halls:of
    stone,:Nine             for:Mortal
   :::Men:::     ________     doomed::to
 die.:One   _,-'...:... `-.    for:::the
 ::Dark::  ,- .:::::::::::. `.   Lord::on
his:dark ,'  .:::::WP::::::.  `.  :throne:
In:::the/    ::::dmmmmmb::::    \ Land::of
:Mordor:\    ::::SAURON:::::    / :where::
::the::: '.  '::::ymmmp::::'  ,'  Shadows:
 lie.::One  `. ``:::::::::'' ,'    Ring::to
 ::rule::    `-._```:'''_,-'     ::them::
 all,::One      `-----'        ring::to
   ::find:::                  them,:One
    Ring:::::to            bring::them
      all::and::in:the:darkness:bind
        them:In:the:Land:of:Mordor
           where:::the::Shadows
                :::lie.:::                                
                                
                                                        v.0.1
"""



def main():
    parser = argparse.ArgumentParser(description="Passively scan a wordpress site and grabs installed plugins. Then creates a test development for static and dynamic code analysis")
    parser.add_argument('domain', help="the domain name to analyze (example: test.com)")
    parser.add_argument('--subdomains', help="include subdomains in the initial passive scan", action='store_true')
    args = parser.parse_args()

    # check if components / requirements are installated and in $PATH
    status, message = initial_checks()
    if not status:
        print("[error]:", message)
        exit(1)

    # init project
    if not validators.domain(args.domain):
        print("[ERROR]: ", "Invalid Domain Name")
        exit(1)
    print(banner)
    print(f"[LOG]: start scanning :)")
    print(f"[LOG]: init the project with name: ",  args.domain)
    p = Project(args.domain, args.subdomains)
    print("[LOG]: done. I'm now searching for plugins in waybackmachine...")
    found_plugins = p.get_plugins()
    n_plugins = len(found_plugins)
    print(f"[LOG]: found {n_plugins} plugins.. ")
    if n_plugins == 0:
        print("[ERROR]: I didn't found wordpress plugins :(. Exiting... ")
        exit(1)
    for p_name in found_plugins:
        print("Found plugin with name: ", p_name)
    print("[LOG]: done. Now I download each plugin inside the project folder: ", p.project_path)
    p.downloads_plugins_and_extract()
    print(f"[LOG]: done. Go to  f{p.project_path} and start a docker-compose :)")




if __name__ == "__main__":
    main()








