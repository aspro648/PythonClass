# Program to create certificates from a list of names.
# Created for EMAG's Introductory Python Courses
# Ken Olsen, June 15th, 2012, kenneth.olsen@hp.com

# Cast Iron (Montey Python like font) available from
# http://moorstation.org/typoasis/designers/westwind/castiron.htm
# or try:
#   VIVALDII.TTF
#   KUNSTLER.TTF
#   BRUSHSCI
#   VLADIMIR

# reportlab package from:
# http://www.reportlab.com/software/opensource/rl-toolkit/download/

from __future__ import division
import Image, ImageDraw, sys, ImageFont, ImageOps
import os, sys

award_date = "June 12th - 21st, 2012"
award_event = "EMAG's Introductory Python Courses"


def loadNames(fName):
    ''' Open names.csv and return a list of names.'''

    print '\nLoading "%s"' % fName
    data_dict = {}
    try:
        data = open(fName, 'r')
    except:
        print "\nCouldn't find %s file!" % fName
        print "Is it in same directory as python script?\n"
        sys.exit()
    for line in data.readlines()[1:]:
        values = line.strip().split(',')
        name = values[0]
        left_mark = values[1]
        right_mark = values[2]
        data_dict[name] = (left_mark, right_mark)
    return data_dict
        
        
def addText(img, text, fontName, fontSize, (x, y)):
    ''' Add centered text to image at (x, y) from center '''
    #im = Image.new('RGB', (730, 54))
    imgX, imgY = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fontName, fontSize)
    xx,yy = draw.textsize(text, font=font)

    # determine offset from center
    x = int((imgX - xx) / 2) + x
    y = int((imgY - yy) / 2) + y
    draw.text((x, y), text, fill='black', font=font)
    del draw
    return img


def addLine(img, (x, y), width):
    ''' add a horizontal line at (x, y) from center '''
    imgX, imgY = img.size
    draw = ImageDraw.Draw(img)

    # determine offset from center
    x = int(imgX / 2 + x - width / 2)
    y = int(imgY /2  + y)
    draw.line([(x, y), (x + width, y)], width=2, fill='black')
    del draw
    return img


def createCert(name, marks):
    ''' creates and saves individual certificates in folder '''
    print '\t -creating certificate for "%s" with %s' % (name, marks)
    # open certificate border
    img = Image.open('award_template.png')

    addText(img, 'Certificate of Completion', 'OLDENGL.TTF', 80, (0, -400))
    
    # add name and award
    award_font = 'Cast Iron.ttf'
    addText(img, 'Python', award_font, 140, (0, -240))
    addText(img, 'Programming', award_font, 110, (0, -80))
    
    addText(img, 'presented to', 'georgiai.ttf', 36, (0, 30))
    if len(name) > 14:
        addText(img, name, 'BRUSHSCI.TTF', 100, (0, 140))
    else:
        addText(img, name, 'BRUSHSCI.TTF', 120, (0, 140))
    addText(img, 'for attending', 'georgiaz.ttf', 32, (0, 230))
    addText(img, award_event, 'georgiab.ttf', 64, (0, 310))
    addText(img, '%s' % award_date, 'georgiai.ttf', 44, (0, 410))

    # add signature lines
    addText(img, 'Instructor', 'georgiai.ttf', 32, (450, 444))
    addLine(img, (450, 424), 420)
    addText(img, 'Instructor', 'georgiai.ttf', 32, (-440, 444))
    addLine(img, (-440, 424), 420)

    LEFT = 0
    RIGHT = 1

    logo = {LEFT: {'xy': (210, 640), 'resize': 1.1},
            RIGHT: {'xy': (1200, 640), 'resize': 1.1}}

    seal = {LEFT: {'xy': (230, 630), 'resize': 0.8},
            RIGHT: {'xy': (1200, 630), 'resize': 0.8}}

    foot = {LEFT: {'xy': (180, 690), 'resize': 0.7},
            RIGHT: {'xy': (1050, 690), 'resize': 0.7}}

    graph = {LEFT: {'xy': (210, 650), 'resize': 1.0},
             RIGHT: {'xy': (1180, 650), 'resize': 1.0}}

    settings =  {'logo': logo, 'seal': seal, 'foot': foot, 'graph': graph}
    #print settings

    for side, mark in enumerate(marks):
        if mark:
            mark_img = Image.open(mark + '.png')
            xy = settings[mark][side]['xy']
            resize = settings[mark][side]['resize']
            mark_img = mark_img.resize((int(mark_img.size[LEFT] * resize),
                                        int(mark_img.size[RIGHT] * resize)))
            if mark == 'foot' and side == LEFT:
                mark_img = ImageOps.mirror(mark_img)
            img.paste(mark_img, xy, mark_img)
        

    # add seal or logo
    if False: # add seal
        seal = Image.open('seal.png')
        seal = seal.resize((int(seal.size[0] * 0.8), int(seal.size[1] * 0.8)))
        img.paste(seal, (230, 630), seal)
    if False: # add logo
        seal = Image.open('Emag_logo.png')
        seal = seal.resize((int(seal.size[0] * 1.1), int(seal.size[1] * 1.1)))
        img.paste(seal, (230, 630), seal)

    # add Montey Python foot
    if False:
        foot = Image.open('foot.png')
        foot = foot.resize((int(foot.size[0] * 0.7), int(foot.size[1] * 0.7)))
        img.paste(foot, (1050, 700), foot)
    if False:
        graph = Image.open('graph.png')
        graph = graph.resize((int(graph.size[0] * 1), int(graph.size[1] * 1)))
        img.paste(graph, (1200, 650), graph)

    # save to 'certificate' folder
    img.save('certificates/%s.png' % name, 'PNG')


if __name__ == '__main__':

    # load name and awards
    data_dict = loadNames('names.csv')

    # make directory if not there
    if not os.path.isdir('certificates'):
        os.mkdir('certificates')
        print 'Created "certificates" directory'
    else:
        print 'Saving to "certificates" directory'

    for name, marks in data_dict.items():
        createCert(name, marks)

