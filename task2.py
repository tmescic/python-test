#!/usr/bin/python2.7
# encoding: utf-8
'''
Created on Dec 15, 2014

Write a script that removes blank paragraphs from HTML document. A blank 
paragraph should be considered to be a <p> </p> tag containing only white spaces.

@author: tmescic
'''

from HTMLParser import HTMLParser

# subclassing HTMLParser and adding logic to remove empty paragraphs
class EmptyPtagRemover(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.empty_p_in_progress = False
        self.empty_p_positions = []
    
    def handle_starttag(self, tag, attrs):
        # handling start of P tag
        if tag == "p":
            self.empty_p_in_progress = True
            self.p_start_pos = self.getpos()
        
    def handle_endtag(self, tag):
        
        # handling end of P tag
        # if this was an empty paragraph, store it's beginning and end 
        # (start_line, star_position, end_line, end_position)
        if tag == "p" and self.empty_p_in_progress:
            self.empty_p_in_progress = False
            self.empty_p_positions.append((self.p_start_pos[0]-1, self.p_start_pos[1], self.getpos()[0]-1, self.getpos()[1]))
        
    def handle_data(self, data):
        if self.empty_p_in_progress and not data.isspace():
            # check that only whitespace is inside a paragraph
            self.empty_p_in_progress = False 
    
    def filter_p(self, in_html):
        """Parses the input HTML and returns the HTML without empty paragraphs""" 
        
        # process the input (find locations of empty Ps)
        self.feed(in_html)
           
        lines = in_html.splitlines(True)
        
        # remove all empty paragraphs one by one
        for pos in reversed(self.empty_p_positions):

            start_line = pos[0]
            start_offset = pos[1]
            
            end_line = pos[2]
            end_offset = pos[3]
        
            if start_line == end_line:
                # empty P is inside a single line
                line = lines[start_line]
                end_offset += line[end_offset:].index('>') + 1  # to handle </p     >
                lines[start_line] = line[:start_offset] + line[end_offset:]
            else:
                # empty P spans two or more lines
                lines[start_line] = lines[start_line][:start_offset]
                
                end_offset += lines[end_line][end_offset:].index('>') + 1 # to handle </p     >
                lines[end_line]   = lines[end_line][end_offset:]
                
                # delete empty lines inside the paragraph
                for i in range (start_line+1, end_line):
                    del lines[i]
            
        return ''.join(lines)
    
    
if __name__ == '__main__':
    
    test_input = """<html><head><title>I am a title</title></head>
<body><h1>I am a heading!</h1><p></p     ><p>


</p>
<p>not empty</p><p    > </p> a <p> a </p><p class="asd"></p></body>
<!-- My comment with an empty <p></p> inside (or why I didn't use regex).... --><p></p></html>"""

    print "Input HTML: "
    print "===========\n", test_input

    # instantiate the parser...
    parser = EmptyPtagRemover()

    # parse input and return HTML without empty paragraphs
    out_html = parser.filter_p(test_input)

    print "\n\nOutput HTML:"
    print "============\n", out_html

