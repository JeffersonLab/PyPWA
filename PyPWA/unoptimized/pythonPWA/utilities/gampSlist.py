# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 14:25:12 2014

@author: sbramlett
"""

import os
import time
import numexpr as ne

from PyPWA.libs.data.builtin import gamp


ne.set_num_threads(4)
class gampSlist(object):
    def __init__(self, indir, gfile):
        self.indir = indir
        self.gfile = gfile
        print(time.time())
        self.events = gamp.GampMemory.parse(os.path.join(indir,gfile) + 'length')
        print(time.time())
        self.eventslist = []

    def generate(self):
        for event in self.events:
            for particles in event.particles:
                if particles.particleID == "14": #proton
                    prE = float(particles.particleE)
                    prpx = float(particles.particleXMomentum)
                    prpy = float(particles.particleYMomentum)
                    prpz = float(particles.particleZMomentum)
                    mp = float((float(particles.particleE)**2 - float(particles.particleXMomentum)**2 -
                         float(particles.particleYMomentum)**2 - float(particles.particleZMomentum)**2)**(1./2.))
                if particles.particleID == "1": #photon
                    phE = float(particles.particleE)
                    phpx = float(particles.particleXMomentum)
                    phpy = float(particles.particleYMomentum)
                    phpz = float(particles.particleZMomentum)
                if particles.particleID == "12": #K-
                    kmE = float(particles.particleE)
                    kmpx = float(particles.particleXMomentum)
                    kmpy = float(particles.particleYMomentum)
                    kmpz = float(particles.particleZMomentum)
                if particles.particleID == "11": #K+
                    kpE = float(particles.particleE)
                    kppx = float(particles.particleXMomentum)
                    kppy = float(particles.particleYMomentum)
                    kppz = float(particles.particleZMomentum)
                    mk = float((float(particles.particleE)**2 - float(particles.particleXMomentum)**2 -
                         float(particles.particleYMomentum)**2 - float(particles.particleZMomentum)**2)**(1./2.))
            sab = (.93827 + phE)**2 - (0 + phpx)**2 - (0 + phpy)**2 - (0 + phpz)**2
            sa1 = (phE - kpE)**2 - (phpx - kppx)**2 - (phpy - kppy)**2 - (phpz - kppz)**2
            s12 = (kpE + kmE)**2 - (kppx + kmpx)**2 - (kppy + kmpy)**2 - (kppz + kmpz)**2
            s23 = (kmE + prE)**2 - (kmpx + prpx)**2 - (kmpy + prpy)**2 - (kmpz + prpz)**2
            sb3 = (.93827 - prE)**2 - (0 - prpx)**2 - (0 - prpy)**2 - (0 - prpz)**2
            slist = [mk, mp, sab, sa1, s12, s23, sb3]
            #print slist
            #print
            self.eventslist.append(slist)
        print(time.time())
        return self.eventslist

    def toFile(self, outputdir, outputFile):
        f = open(os.path.join(outputdir, outputFile), 'w')
        f.write(str(len(self.events)) + "\n")
        for slist in self.eventslist:
            f.write(str(slist) + "\n")
        f.close()


