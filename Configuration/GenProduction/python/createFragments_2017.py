#!/usr/bin/env python
import os
import sys
import random
import argparse
import json
import shutil
import subprocess


def create_config(input_jsonfile):
	with open(input_jsonfile) as data_file:
		data = json.load(data_file)
		for sample, sample_cfg in data.items():
			directory = sample_cfg["dir"]
			print "creating directory:", directory
			os.makedirs(directory)
			tarball = sample_cfg["tarball"]
			pre_ext = sample_cfg["pre_ext"]
			FilePrep="""
import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('%s'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(True),
)

import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        pythia8PowhegEmissionVetoSettingsBlock,
        processParameters = cms.vstring(
            'SpaceShower:pTmaxMatch = 1',
            'TimeShower:pTmaxMatch = 1',
            'ParticleDecays:allowPhotonRadiation = on',
            'TimeShower:QEDshowerByL = off',
            'BeamRemnants:hardKTOnlyLHE = on',
            'BeamRemnants:primordialKThard = 2.225001',
            'SpaceShower:dipoleRecoil = 1',
            ),
                parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters')
    ),
        ExternalDecays = cms.PSet(
        Photospp = cms.untracked.PSet(
            parameterSets = cms.vstring("setExponentiation", "setInfraredCutOff", "setMeCorrectionWtForW", "setMeCorrectionWtForZ", "setMomentumConservationThreshold", "setPairEmission", "setPhotonEmission", "setStopAtCriticalError", "suppressAll", "forceBremForDecay"),
            setExponentiation = cms.bool(True),
            setMeCorrectionWtForW = cms.bool(True),
            setMeCorrectionWtForZ = cms.bool(True),
            setInfraredCutOff = cms.double(0.00011),
            setMomentumConservationThreshold = cms.double(0.1),
            setPairEmission = cms.bool(True),
            setPhotonEmission = cms.bool(True),
            setStopAtCriticalError = cms.bool(False),
            # Use Photos only for W/Z decays
            suppressAll = cms.bool(True),
            forceBremForDecay = cms.PSet(
                parameterSets = cms.vstring("Z", "Wp", "Wm"),
                Z = cms.vint32(0, 23),
                Wp = cms.vint32(0, 24),
                Wm = cms.vint32(0, -24),
            ),
        ),
        parameterSets = cms.vstring("Photospp")
    )
)

ProductionFilterSequence = cms.Sequence(generator)
"""%(tarball)
			print "creating Fragments for this directory"
			f=open(os.path.join(directory, pre_ext + '.py'), 'w+')
			f.write(FilePrep)
			f.close()
def main():
	from argparse import ArgumentParser
	import argparse
	parser = ArgumentParser(description="Do -h to see usage")
	parser.add_argument('-i', '--json', type=str)
	args = parser.parse_args()
	print(args)
	create_config(args.json)


if __name__ == "__main__":
	main()
