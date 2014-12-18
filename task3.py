#!/usr/bin/python2.7
# encoding: utf-8
'''
Created on Dec 17, 2014

Write a decorator that stores the result of a function call and returns the cached version in
subsequent calls (with the same parameters) for 5 minutes, or ten times ­­ whichever comes
first.

@author: tmescic
'''

import datetime

def cache_func(func):
    """ Decorator that caches result of function calls"""
    
    g = func.func_globals
    
    def func_wrapper(*v, **k):
        
        # we will use input arguments (v) as a dictionary key for storing our counter and time
        if not g.has_key(v):
            g[v] = {}

        gv = g[v]
        
        # increase counter (or initialize for first call)
        gv['counter'] = (gv['counter'] + 1) % 11 if gv.has_key('counter') else 0
        
        if (gv['counter'] == 0 or (datetime.datetime.now() - gv['last_update_time']).total_seconds() > 300):
            
            # we need to update cache (and reset timer and update time)
            
            gv['cached_value'] = func(*v, **k)   # call fn and update cached value 
            gv['counter'] = 0 # reset counter
            gv['last_update_time'] = datetime.datetime.now()
            print "Cache updated : ", gv['cached_value']
        else:
            print "From cache    : ", gv['cached_value']

        return gv['cached_value']
    
    return func_wrapper


@cache_func
def fibb(n):
    """ Calculates the nth fibonacci number."""
    prev = 1
    curr = 1
    for i in range(1, n-1):
        tmp = curr
        curr += prev
        prev = tmp
        
    return curr

@cache_func
def take_two(a, b):
    return a + b

if __name__ == '__main__':

    for i in range (13):
        fibb(8)
        
    fibb(9)
    fibb(10)
    fibb(17)
    fibb(18)
    
    for i in range (11):
        take_two(12, 34)
        take_two(34, 12)
    
