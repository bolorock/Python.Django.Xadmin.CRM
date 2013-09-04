'''
Created on 2013-8-21

@author: hgq
'''
import time

def generate_code(prefix):
    return prefix+ time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))